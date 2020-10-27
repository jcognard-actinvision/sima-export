####
# This script demonstrates how to export a view using the Tableau
# Server Client.
#
# To run the script, you must have installed Python 3.5 or later.
####

import argparse
import logging
import os
import sys
import urllib3
import csv
import io

import tableauserverclient as TSC


def transform_csv(input):
    with open('tmp.csv', 'wb') as f:
        f.writelines(input)

    with open('tmp.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        transformed = io.StringIO(newline="\n")
        csv.writer(transformed, delimiter=';',
                   quoting=csv.QUOTE_NONE).writerows(reader)
        ret = transformed.getvalue()
        transformed.close()

    os.remove('tmp.csv')

    return ret


def main():
    # disable SSL warning
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(
        description='Export a view as an image, PDF, or CSV')
    parser.add_argument('--server', '-s', required=True, help='server address')
    parser.add_argument('--site', '-S', default=None)
    parser.add_argument('--token-name', '-n', required=True,
                        help='username to signin under')
    parser.add_argument(
        '--token', '-t', help='personal access token for logging in')

    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')

    parser.add_argument(
        '--file', '-f', help='filename to store the exported data')
    parser.add_argument('first_resource_id', help='LUID for the first view')
    parser.add_argument('second_resource_id', help='LUID for the second view')

    args = parser.parse_args()
    token = os.environ.get('TOKEN', args.token)
    if not token:
        print("--token or TOKEN environment variable needs to be set")
        sys.exit(1)

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # SIGN IN
    tableau_auth = TSC.PersonalAccessTokenAuth(
        args.token_name, token, site_id=args.site)
    server = TSC.Server(args.server)
    # Disable SSL verification for now
    server.add_http_options({'verify': False})
    # Use highest API version possible
    server.use_server_version()

    with server.auth.sign_in(tableau_auth):
        # Get first line
        views = filter(lambda x: x.id == args.first_resource_id,
                       TSC.Pager(server.views.get))
        view = list(views).pop()
        server.views.populate_csv(view)
        lines = [transform_csv(view.csv).split("\n")[1]]

        # Get following lines
        views = filter(lambda x: x.id == args.second_resource_id,
                       TSC.Pager(server.views.get))
        view = list(views).pop()
        server.views.populate_csv(view)
        lines.extend(transform_csv(view.csv).split("\n")[1:])

        if args.file:
            filename = args.file
        else:
            filename = 'out.csv'

        with open(filename, 'w') as f:
            f.writelines(lines)


if __name__ == '__main__':
    main()
