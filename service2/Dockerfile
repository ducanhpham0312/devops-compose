# Use the official Golang image
FROM golang:1.23

# Set the working directory
WORKDIR /app

# Copy the application code
COPY service2.go .

# Build the Go application
RUN go build -o service2 service2.go

# Expose the port
EXPOSE 8200

# Run the application
CMD ["./service2"]
