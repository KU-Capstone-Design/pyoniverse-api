import os
import traceback

import dotenv


dotenv.load_dotenv()
import json
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Chalice deploy script",
    )
    parser.add_argument("--stage", type=str)
    args = parser.parse_args()

    # load config file
    with open(r".chalice/config.json", "r") as f:
        config = json.load(f)

    # backup config file
    with open(r".chalice/config.json.bak", "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    try:
        # update config file
        config["manage_iam_role"] = False
        config["iam_role_arn"] = os.getenv("IAM_ROLE_ARN")
        if "environment_variables" not in config["stages"][args.stage]:
            config["stages"][args.stage]["environment_variables"] = {}
        config["stages"][args.stage]["environment_variables"]["MONGO_URI"] = os.getenv(
            "MONGO_URI"
        )
        config["stages"][args.stage]["environment_variables"][
            "DB_QUEUE_NAME"
        ] = os.getenv("DB_QUEUE_NAME")
        config["stages"][args.stage]["api_gateway_custom_domain"][
            "domain_name"
        ] = os.getenv("DOMAIN_NAME")
        config["stages"][args.stage]["api_gateway_custom_domain"][
            "certificate_arn"
        ] = os.getenv("CERTIFICATE_ARN")

        # save config file
        with open(r".chalice/config.json", "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        # deploy
        os.system(f"chalice deploy --stage {args.stage}")
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Error: {tb}")
    finally:
        # rollback config file
        with open(r".chalice/config.json.bak", "r") as f:
            config = json.load(f)
        with open(r".chalice/config.json", "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        # remove backup file
        os.remove(r".chalice/config.json.bak")
