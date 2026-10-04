import socket
import time
import random

HOST = "127.0.0.1"
PORT = 5000

WINDOW_SIZE = 4
TOTAL_FRAMES = 10

# Simulate packet loss
LOSS_PROBABILITY = 0.20

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.settimeout(2)

receiver_address = (HOST, PORT)

print("=" * 50)
print("       GO-BACK-N SENDER")
print("=" * 50)

print(f"Receiver: {HOST}:{PORT}")
print(f"Window Size: {WINDOW_SIZE}")
print(f"Total Frames: {TOTAL_FRAMES}")
print(f"Packet Loss Probability: {LOSS_PROBABILITY * 100}%")
print("=" * 50)

base = 0
next_frame = 0

while base < TOTAL_FRAMES:

    print(f"\nCurrent Window: ", end="")

    for i in range(base, min(base + WINDOW_SIZE, TOTAL_FRAMES)):
        print(i, end=" ")

    print()

    # Send frames inside the window
    while next_frame < base + WINDOW_SIZE and next_frame < TOTAL_FRAMES:

        print(f"Sending Frame {next_frame}")

        # Simulate frame loss
        if random.random() < LOSS_PROBABILITY:

            print(f"*** Frame {next_frame} LOST ***")

        else:

            sender_socket.sendto(
                str(next_frame).encode(),
                receiver_address
            )

        next_frame += 1
        time.sleep(0.5)

    # Wait for ACK
    try:

        data, address = sender_socket.recvfrom(1024)

        ack_message = data.decode()

        print(f"Received: {ack_message}")

        if ack_message.startswith("ACK:"):

            ack_number = int(ack_message.split(":")[1])

            if ack_number >= base:

                base = ack_number + 1

    except socket.timeout:

        print("\n!!! TIMEOUT !!!")
        print(f"Go-Back-N: Retransmitting from Frame {base}")

        next_frame = base

print("\n" + "=" * 50)
print("All frames transmitted successfully!")
print("=" * 50)

sender_socket.sendto(
    b"END",
    receiver_address
)

sender_socket.close()