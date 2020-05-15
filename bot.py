import csv
import os
import random
import sys
from timeit import default_timer as timer

import factory
import requests
import yaml


class NaviBotService:
    config_file_name = 'bot_config.yaml'
    users_file_name = 'users.csv'
    posts_file_name = 'posts.csv'
    likes_file_name = 'likes.csv'

    def get_config(self):
        with open(self.config_file_name) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config

    def sign_up_users(self):
        config = self.get_config()
        sign_up_url = config['api_base_url'] + config['api_auth_register_url']
        users_lists = []

        for idx in range(config['number_of_users']):
            password = factory.Faker('password').generate()
            data = {
                'email': factory.Faker('free_email').generate(),
                'password1': password,
                'password2': password,
            }
            response = requests.post(sign_up_url, data=data)

            if response.status_code == requests.codes.created:
                data = response.json()

                users_lists.append({
                    'id': data.get('user', {}).get('id'),
                    'auth_token': data.get('key'),
                    'email': data.get('user', {}).get('email'),
                })

        if users_lists:
            self.write_csv(
                file_name=self.users_file_name,
                fieldnames=['id', 'auth_token', 'email'],
                rows=users_lists,
            )

    def create_posts(self):
        users = self.read_csv(self.users_file_name)
        config = self.get_config()
        post_create_url = config['api_base_url'] + config['api_posts_create_url']
        posts_list = []

        for user in users:

            for idx in range(config['max_posts_per_user']):
                data = {
                    'title': factory.Faker('word').generate().title(),
                    'content': factory.Faker('paragraph').generate(),
                }
                response = requests.post(
                    post_create_url, data=data,
                    headers=self.format_auth_headers(user.get('auth_token')),
                )

                if response.status_code == requests.codes.created:
                    data = response.json()

                    posts_list.append({
                        'id': data.get('id'),
                        'title': data.get('title'),
                        'author_id': user.get('author_id')
                    })

        if posts_list:
            self.write_csv(
                file_name=self.posts_file_name,
                fieldnames=['id', 'title', 'author_id'],
                rows=posts_list,
            )

    def create_likes(self):
        config = self.get_config()
        like_create_url = config['api_base_url'] + config['api_likes_create_url']
        max_likes_per_user = config['max_likes_per_user']
        users = self.read_csv(self.users_file_name)
        posts = self.read_csv(self.posts_file_name)
        likes_list = []

        for user in users:
            likes_counter = 0
            for post in random.choices(posts, k=len(posts) // 2):
                if likes_counter == max_likes_per_user:
                    break
                data = {
                    'content_object': post.get('id'),
                }
                response = requests.post(
                    like_create_url, data=data,
                    headers=self.format_auth_headers(user.get('auth_token')),
                )
                likes_counter += 1

                if response.status_code == requests.codes.created:
                    data = response.json()
                    likes_list.append({
                        'id': data.get('id'),
                        'post_id': data.get('content_object'),
                        'added_by': user.get('id'),
                    })

        if likes_list:
            self.write_csv(
                file_name=self.likes_file_name,
                fieldnames=['id', 'post_id', 'added_by'],
                rows=likes_list,
            )

    def write_csv(self, file_name, fieldnames, rows):
        with open(file_name, mode='w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for row in rows:
                csv_writer.writerow(row)

    def read_csv(self, file_name):
        users_data = []
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                users_data.append(row)
        return users_data

    def format_auth_headers(self, auth_token):
        return {
            'Accept': 'application/json',
            'Authorization': f'Token {auth_token}'
        }

    def get_statistic(self):
        total_users = len(self.read_csv(self.users_file_name))
        total_posts = len(self.read_csv(self.posts_file_name))
        total_likes = len(self.read_csv(self.likes_file_name))

        sys.stdout.write(f'Total users signed up: {total_users}\n')
        sys.stdout.write(f'Total posts created: {total_posts}\n')
        sys.stdout.write(f'Total likes left: {total_likes}\n')

    def clean_up(self):
        os.remove(self.users_file_name)
        os.remove(self.posts_file_name)
        os.remove(self.likes_file_name)
        sys.stdout.write('Clean up files...\n')

    def do_fire(self):
        bot_started = timer()
        sys.stdout.write('Process starting...\n')
        self.sign_up_users()
        self.create_posts()
        self.create_likes()
        self.get_statistic()
        self.clean_up()
        bot_stopped = timer()
        sys.stdout.write(f'Jobs completed. Execution time: {abs(round(bot_started - bot_stopped, 3))} sec.\n')


if __name__ == '__main__':
    navi_bot = NaviBotService()
    navi_bot.do_fire()
