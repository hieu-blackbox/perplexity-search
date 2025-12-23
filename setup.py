from setuptools import setup, find_packages

setup(
    name="perplexity-search-mcp",
    version="1.0.0",
    description="Model Context Protocol server for Perplexity's web search",
    author="",
    author_email="",
    url="https://github.com/yourusername/perplexity-search-mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=0.9.0",
        "httpx>=0.27.0",
        "python-dotenv>=1.0.0",
        "starlette>=0.37.0",
        "uvicorn>=0.30.0",
    ],
    entry_points={
        "console_scripts": [
            "perplexity-search-mcp=server:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
