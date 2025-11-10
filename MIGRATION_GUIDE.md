# Database Migration Guide

## Overview
This guide covers database schema migrations, versioning, and rollback procedures.

## Migration Workflow

### Creating Migrations
```bash
# Create new migration
python manage.py makemigrations myapp

# With descriptive name
python manage.py makemigrations myapp --name add_user_email_index

# Create empty migration
python manage.py makemigrations --empty myapp --name custom_migration
```

### Applying Migrations
```bash
# Apply all pending migrations
python manage.py migrate

# Apply specific migration
python manage.py migrate myapp 0005_migration_name

# Apply migrations to specific app
python manage.py migrate myapp

# Show migration status
python manage.py showmigrations
```

## Migration Examples

### Adding a Field
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(
                max_length=20,
                null=True,
                blank=True
            ),
        ),
    ]
```

### Adding an Index
```python
class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0002_user_phone_number'),
    ]
    
    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(
                fields=['email'],
                name='user_email_idx'
            ),
        ),
    ]
```

### Renaming a Field
```python
class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0003_user_email_index'),
    ]
    
    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
```

### Removing a Field
```python
class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0004_user_phone_rename'),
    ]
    
    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
```

## Data Migrations

### Transform Existing Data
```python
from django.db import migrations

def copy_data(apps, schema_editor):
    User = apps.get_model('myapp', 'User')
    for user in User.objects.all():
        user.new_field = user.old_field.upper()
        user.save()

def reverse_copy(apps, schema_editor):
    User = apps.get_model('myapp', 'User')
    User.objects.all().update(new_field='')

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0005_user_new_field'),
    ]
    
    operations = [
        migrations.RunPython(copy_data, reverse_copy),
    ]
```

## Large Table Migrations

### Safe Migration of Large Tables
```python
# 1. Add column as nullable
python manage.py migrate

# 2. Backfill data in batches
def backfill_large_table(apps, schema_editor):
    User = apps.get_model('myapp', 'User')
    batch_size = 1000
    
    for i in range(0, User.objects.count(), batch_size):
        batch = User.objects.all()[i:i+batch_size]
        for user in batch:
            user.new_field = compute_value(user)
        User.objects.bulk_update(batch, ['new_field'])

# 3. Make column NOT NULL after backfill
# 4. Create indexes
```

## Rollback Procedures

### Rollback Last Migration
```bash
# See current migration
python manage.py showmigrations myapp

# Rollback to specific migration
python manage.py migrate myapp 0004
```

### Emergency Rollback
```bash
# For production emergencies
python manage.py migrate myapp ZERO  # Rollback all

# Or to specific version
python manage.py migrate myapp 0003
```

## Best Practices

### Pre-Migration Checklist
- [ ] Backup database
- [ ] Test migration in staging
- [ ] Plan maintenance window
- [ ] Prepare rollback plan
- [ ] Notify stakeholders
- [ ] Monitor performance

### During Migration
- [ ] Monitor database performance
- [ ] Check application logs
- [ ] Validate data integrity
- [ ] Monitor disk space
- [ ] Have rollback ready

### Post-Migration
- [ ] Verify data integrity
- [ ] Check application functionality
- [ ] Monitor performance metrics
- [ ] Document any issues
- [ ] Communicate completion

## Handling Conflicts

### Merging Migration Conflicts
```bash
# When multiple migrations created in parallel
python manage.py makemigrations --merge

# Review and test the merge migration
python manage.py migrate
```

## Migration Naming Convention
- `0001_initial.py` - Initial schema
- `0002_add_user_email.py` - Specific change
- `0003_rename_user_name.py` - Rename operations
- `0004_populate_data.py` - Data transformations
- `0005_create_indexes.py` - Performance optimizations

## Testing Migrations

### Test Forward Migration
```bash
python manage.py migrate
```

### Test Rollback
```bash
python manage.py migrate myapp 0001
python manage.py migrate myapp
```

### Test in New Database
```bash
python manage.py migrate --run-syncdb
```

## Performance Considerations

- Large index operations may lock tables
- Data migrations on large tables are slow
- Plan migrations during low-traffic periods
- Use batch processing for data updates
- Monitor disk space during migrations
- Consider online migration tools for large tables

## Common Issues

### Issue: Migration Conflicts
**Solution**: Use `makemigrations --merge`

### Issue: Slow Migration
**Solution**: Break into smaller migrations, use batching

### Issue: Migration Won't Reverse
**Solution**: Create manual data migration with proper reverse logic

### Issue: Circular Dependencies
**Solution**: Refactor model dependencies
