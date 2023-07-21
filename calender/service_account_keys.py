# import argparse
# import os
# from google.oauth2 import service_account
# import googleapiclient.discovery  # type: ignore

# # [END iam_create_key]
# # [END iam_list_keys]
# # [END iam_delete_key]

# # [START iam_create_key]
# def create_key(service_account_email: str) -> None:
#     """Creates a key for a service account."""
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/rb211/capestone/bookMeni/key.json"
#     credentials = service_account.Credentials.from_service_account_file(
#         filename=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
#         scopes=["https://www.googleapis.com/auth/cloud-platform"],
#     )

#     service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

#     key = (
#         service.projects()
#         serviceAccounts()
#         .keys()
#         .create(name="projects/-/serviceAccounts/" + service_account_email, body={})
#         .execute()
#     )

#     # The privateKeyData field contains the base64-encoded service account key
#     # in JSON format.
#     json_key_data = key.get('privateKeyData', '')

#     if not key.get("disabled", True):
#         # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable with the file path
#         # where you want to store the key
#         file_path = '/path/to/your/key.json'  # Replace with the desired file path
#         with open(file_path, 'w') as f:
#             f.write(json_key_data)

#         # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the file path
#         os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file_path

#         print("Created and stored JSON key")

#     # create_key('google-calendar@bookmeni.iam.gserviceaccount.com')
# # [END iam_create_key]


# # [START iam_list_keys]
# def list_keys(service_account_email: str) -> None:
#     """Lists all keys for a service account."""
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/rb211/capestone/bookMeni/key.json"
#     credentials = service_account.Credentials.from_service_account_file(
#         filename=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
#         scopes=["https://www.googleapis.com/auth/cloud-platform"],
#     )

#     service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

#     keys = (
#         service.projects()
#         .serviceAccounts()
#         .keys()
#         .list(name="projects/-/serviceAccounts/" + service_account_email)
#         .execute()
#     )

#     for key in keys["keys"]:
#         print("Key: " + key["name"])


# # [END iam_list_keys]


# # [START iam_delete_key]
# # def delete_key(full_key_name: str) -> None:
# #     """Deletes a service account key."""
# #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/rb211/capestone/bookMeni/key.json"
# #     credentials = service_account.Credentials.from_service_account_file(
# #         filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
# #         scopes=["https://www.googleapis.com/auth/cloud-platform"],
# #     )

# #     service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

# #     service.projects().serviceAccounts().keys().delete(name=full_key_name).execute()

# #     print("Deleted key: " + full_key_name)


# # [END iam_delete_key]


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
#     )

#     subparsers = parser.add_subparsers(dest="command")

#     create_key_parser = subparsers.add_parser("create", help=create_key.__doc__)
#     create_key_parser.add_argument("service_account_email")

#     list_keys_parser = subparsers.add_parser("list", help=list_keys.__doc__)
#     list_keys_parser.add_argument("service_account_email")

#     delete_key_parser = subparsers.add_parser("delete", help=delete_key.__doc__)
#     delete_key_parser.add_argument("full_key_name")

#     args = parser.parse_args()

#     if args.command == "list":
#         list_keys(args.service_account_email)
#     elif args.command == "create":
#         create_key(args.service_account_email)
#     elif args.command == "delete":
#         delete_key(args.full_key_name)