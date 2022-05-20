from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="remote-crafter",
    version="0.1.0",
    author="Hafiz Gohar",
    author_email="hafizgohardev@gmail.com",
    description="A comprehensive AI/ML and full-stack development platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/remote-crafter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "django>=4.2.0",
        "djangorestframework>=3.14.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.21.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "tensorflow>=2.12.0",
        "torch>=2.0.0",
        "transformers>=4.28.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "redis>=4.5.0",
        "celery>=5.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.0",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "remote-crafter=remote_crafter.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
