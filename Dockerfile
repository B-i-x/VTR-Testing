# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set non-interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

# Install tzdata package non-interactively
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata


# Install dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    build-essential \
    git \
    python3 \
    python3-pip \
    wget \
    make \
    && rm -rf /var/lib/apt/lists/*



RUN git clone https://github.com/verilog-to-routing/vtr-verilog-to-routing.git /vtr-verilog-to-routing

# Set the working directory
WORKDIR /vtr-verilog-to-routing

# Initialize and update git submodules
RUN git submodule init && git submodule update
RUN ./install_apt_packages.sh

RUN chmod +x install_apt_packages.sh && ./install_apt_packages.sh

# Optionally, set up a Python virtual environment
RUN python3 -m pip install --upgrade pip && \
    python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt

# Compile VTR
RUN make

# Expose the default port the app runs on
EXPOSE 8080

# Set the default command to execute when creating a new container
CMD ["bash"]