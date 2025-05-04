# Use a pre-built Wine image
FROM scottyhardy/docker-wine:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV WINEARCH=win64
ENV WINEPREFIX=/root/.wine

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set up Wine
RUN winecfg && \
    winetricks -q corefonts && \
    winetricks -q msxml6 && \
    winetricks -q vcrun2015 && \
    winetricks -q dotnet48

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 