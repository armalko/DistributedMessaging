import key_utils

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <generate keys? (Y/N)> <client_name_1> <client_name_2>")
        sys.exit(1)

    gen_keys = sys.argv[1]
    client_1 = sys.argv[2]
    client_2 = sys.argv[3]

    if gen_keys not in ["Y", "N"]:
        print("Usage: python3 main.py <generate keys? (Y/N)> <client_name_1> <client_name_2>")
        sys.exit(1)

    if gen_keys == "Y":
        private_key, public_key = key_utils.generate_keys()
        key_utils.save_keys_to_files(private_key, public_key,
                                     f"{client_1}_PRIVATE.pem", f"{client_1}_PUBLIC.pem")

        private_key, public_key = key_utils.generate_keys()
        key_utils.save_keys_to_files(private_key, public_key,
                                     f"{client_2}_PRIVATE.pem", f"{client_2}_PUBLIC.pem")

        print("Keys successfully generated.")

