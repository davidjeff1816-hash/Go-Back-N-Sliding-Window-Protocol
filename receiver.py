import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print("     GO-BACK-N RECEIVER")
print("=" * 50)
print(f"Receiver listening on {HOST}:{PORT}")
print("Waiting for frames...\n")

expected_frame = 0

while True:

    data, sender_address = server_socket.recvfrom(1024)

    message = data.decode()

    if message == "END":
        print("\nTransmission completed.")
        break

    frame_number = int(message)

    print(f"Received Frame: {frame_number}")

    if frame_number == expected_frame:

        print(f"Frame {frame_number} accepted.")

        ack = f"ACK:{frame_number}"
        server_socket.sendto(
            ack.encode(),
            sender_address
        )

        expected_frame += 1

    else:

        print(
            f"Frame {frame_number} discarded "
            f"(Expected {expected_frame})"
        )

        # Send ACK for the last correctly received frame
        last_ack = expected_frame - 1

        ack = f"ACK:{last_ack}"

        server_socket.sendto(
            ack.encode(),
            sender_address
        )

server_socket.close()

print("\nReceiver stopped.")