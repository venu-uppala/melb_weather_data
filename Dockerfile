# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /melb_weather_data

# Copy project files
COPY . /melb_weather_data

# Set PYTHONPATH so 'src' is recognized as a package
ENV PYTHONPATH=/melb_weather_data



# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Default command
CMD ["python3","-m","src.pipeline"]
