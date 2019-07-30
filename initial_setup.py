import os
import random
import re
import subprocess
from jinja2 import Template


DEFAULT_PROJECT_NAME = 'django_project'
PROJECT_SLUG = raw_input('Enter your project\'s slug: ') or 'meh_project'
PROJECT_NAME = raw_input('Enter your project\'s name: ') or 'Meh Project'
ADMIN_NAME = raw_input('Provide the admin\'s name: ') or 'Eshan Das'
ADMIN_EMAIL = raw_input('Provide the admin\'s email: ') or 'eshandasnit@gmail.com'
DB_URI = raw_input('Enter database URI (postgresql://{{user}}:{{password}}@{{host}}:{{port}}/{{dbname}}): ') or 'postgresql://eshan:charli3!@127.0.0.1:9000/meh'


def _get_list_of_files(dir_name):
    '''
    For the given path, get the List of all files in the directory tree 
    '''
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dir_name)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + _get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


# Refresh all SECRET_KEYs in the settings files
def generate_secret_keys():
    print('Generating Django secret keys...')
    file_names = ('local.py', 'production.py')

    for file_name in file_names:
        target_file = open(
            '%s/main/settings/%s' % (DEFAULT_PROJECT_NAME, file_name), mode='r')
        template = Template(target_file.read())
        target_file.close()

        context = {
            'secret_key': ''.join([random.SystemRandom().choice(
                'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])}

        content = template.render(context) + '\n'

        target_file = open(
            '%s/main/settings/%s' % (DEFAULT_PROJECT_NAME, file_name), mode='w')
        target_file.write(content)
        target_file.close()


# Replace "{{django_project}}" with the project name from production.yml and local.yml
def create_docker_compose_files():
    print('Creating docker compose files...')
    file_names = ('local.yml', 'production.yml')

    for file_name in file_names:
        target_file = open(
            '%s' % file_name, mode='r')
        template = Template(target_file.read())
        target_file.close()

        context = {
            'project_slug': PROJECT_SLUG}

        content = template.render(context) + '\n'

        target_file = open(
            '%s' % file_name, mode='w')
        target_file.write(content)
        target_file.close()


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

    context = {
        'project_slug': PROJECT_SLUG,
        'db_uri': DB_URI,
        'admin_email': ADMIN_EMAIL}

    content = template.render(context) + '\n'

    target_file = open('%s/.env' % DEFAULT_PROJECT_NAME, mode='w')
    target_file.write(content)
    target_file.close()


# Prepare template files
def prep_template_files():
    print('Prepare template files...')
    file_names = (
        '%s/templates/site_templates/email_master.html' % DEFAULT_PROJECT_NAME,
        '%s/templates/site_templates/site_master.html' % DEFAULT_PROJECT_NAME,
        '%s/templates/site_templates/blank_page.html' % DEFAULT_PROJECT_NAME,
        '%s/templates/index.html' % DEFAULT_PROJECT_NAME,)

    for file_name in file_names:
        target_file = open(file_name, mode='r')
        template = target_file.read()
        target_file.close()

        content = re.sub('{{\s*project_slug\s*}}', PROJECT_SLUG, template)  # noqa
        content = re.sub('{{\s*project_name\s*}}', PROJECT_NAME, template)  # noqa

        target_file = open(file_name, mode='w')
        target_file.write(content)
        target_file.close()


# Prepare other files as well
def prep_other_files():
    print('Prepare other files...')
    file_names = (
        '%s/main/urls.py' % DEFAULT_PROJECT_NAME,)

    for file_name in file_names:
        target_file = open(file_name, mode='r')
        template = Template(target_file.read())
        target_file.close()

        context = {
            'project_slug': PROJECT_SLUG,
            'project_name': PROJECT_NAME}

        content = template.render(context) + '\n'

        target_file = open(file_name, mode='w')
        target_file.write(content)
        target_file.close()


# Prepare docker files
def prep_docker_files():
    print('Prepare Docker files...')
    file_names = _get_list_of_files('./compose')

    for file_name in file_names:
        target_file = open(file_name, mode='r')
        template = Template(target_file.read())
        target_file.close()

        context = {
            'project_slug': PROJECT_SLUG,
            'project_name': PROJECT_NAME}

        content = template.render(context) + '\n'

        target_file = open(file_name, mode='w')
        target_file.write(content)
        target_file.close()


# Setup flake8
def setup_flake8():
    # http://flake8.pycqa.org/en/latest/user/using-hooks.html
    print('Setup flake8...')
    subprocess.run(["flake8", "--install-hook", "git"], capture_output=True)
    subprocess.run(["git config", "--bool", "flake8.strict", "true"], capture_output=True)


# Rename the "django_project" folder name
def rename_project_folder():
    os.rename('django_project', PROJECT_SLUG)


def main():
    generate_secret_keys()
    create_docker_compose_files()
    create_env_file()
    prep_other_files()
    prep_template_files()
    prep_docker_files()
    setup_flake8()
    rename_project_folder()


if __name__ == '__main__':
    main()
