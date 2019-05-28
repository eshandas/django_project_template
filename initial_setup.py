import os
import random
from jinja2 import Template


DEFAULT_PROJECT_NAME = 'django_project'
PROJECT_SLUG = input('Enter your project\'s slug: ')
PROJECT_NAME = input('Enter your project\'s name: ')
ADMIN_NAME = input('Provide the admin\'s name: ')
ADMIN_EMAIL = input('Provide the admin\'s email: ')
DB_URI = input('Enter database URI (postgresql://{{user}}:{{password}}@{{host}}:{{port}}/{{dbname}}): ')


# Refresh all SECRET_KEYs in the settings files
def generate_secret_keys():
    print('Generating Django secret keys...')
    file_names = ('local.py', 'production.py')

    for file_name in file_names:
        setting_file = open(
            '%s/main/settings/%s' % (DEFAULT_PROJECT_NAME, file_name), mode='r')
        template = Template(setting_file.read())
        setting_file.close()

        context = {
            'secret_key': ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])}

        content = template.render(context) + '\n'

        setting_file = open(
            '%s/main/settings/%s' % (DEFAULT_PROJECT_NAME, file_name), mode='w')
        setting_file.write(content)
        setting_file.close()


# Replace "{{django_project}}" with the project name from production.yml and local.yml
def create_docker_compose_files():
    print('Creating docker compose files...')
    file_names = ('local.yml', 'production.yml')

    for file_name in file_names:
        setting_file = open(
            '%s' % file_name, mode='r')
        template = Template(setting_file.read())
        setting_file.close()

        context = {
            'project_slug': PROJECT_SLUG}

        content = template.render(context) + '\n'

        setting_file = open(
            '%s' % file_name, mode='w')
        setting_file.write(content)
        setting_file.close()


# Create .env file
def create_env_file():
    print('Creating env file...')

    template = Template('''
# DATABASES
DATABASE_URL={{db_uri}}

# AWS
AWS_ACCESS_KEY=xxxxxxxxxxxxxxxxxxx
AWS_ACCESS_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=us-west-2

# EMAIL
EMAIL_HOST=email-smtp.us-west-2.amazonaws.com
EMAIL_PORT=465
EMAIL_HOST_USER=xxxxxxxxxxxxxxxxxxx
EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EMAIL_FROM={{admin_email}}

# ENVIRONMENT
VIRTUALENV={{project_slug}}
''')

    # setting_file = open('%s/.env' % DEFAULT_PROJECT_NAME, mode='r')
    # setting_file.close()

    context = {
        'project_slug': PROJECT_SLUG,
        'db_uri': DB_URI,
        'admin_email': ADMIN_EMAIL}

    content = template.render(context) + '\n'

    setting_file = open('%s/.env' % DEFAULT_PROJECT_NAME, mode='w')
    setting_file.write(content)
    setting_file.close()


# Prepare other files as well
def prep_other_files():
    print('Prepare other files...')
    file_names = (
        '%s/main/urls.py' % DEFAULT_PROJECT_NAME,)

    for file_name in file_names:
        setting_file = open(file_name, mode='r')
        template = Template(setting_file.read())
        setting_file.close()

        context = {
            'project_slug': PROJECT_SLUG,
            'project_name': PROJECT_NAME}

        content = template.render(context) + '\n'

        setting_file = open(file_name, mode='w')
        setting_file.write(content)
        setting_file.close()


# Rename the "django_project" folder name
def rename_project_folder():
    os.rename('django_project', PROJECT_SLUG)


def main():
    generate_secret_keys()
    create_docker_compose_files()
    create_env_file()
    prep_other_files()
    rename_project_folder()


if __name__ == '__main__':
    main()
