import os

from flask import Flask
import pexpect

app = Flask(__name__)


class Ssh(object):

    client = None

    @classmethod
    def connect(cls, ip, username="root", password="admin", prompt=']#',
                silent=False):

        # Ssh to remote server
        ssh_newkey = 'Are you sure you want to continue connecting'
        child = pexpect.spawn('ssh ' + username + '@' + ip, maxread=5000)

        i = 1
        # Enter password
        while i != 0:
            i = child.expect([prompt, 'assword:*', ssh_newkey, pexpect.TIMEOUT,
                              'key.*? failed'])
            if not silent:
                print child.before, child.after,
            if i == 0:  # find prompt
                pass
            elif i == 1:  # Enter password
                child.send(password + "\r")
            if i == 2:  # SSH does not have the public key. Just accept it.
                child.sendline('yes\r')
            if i == 3:  # Timeout
                raise Exception('ERROR TIMEOUT! SSH could not login. ')
            if i == 4:  # new key
                print child.before, child.after,
                os.remove(os.path.expanduser('~') + '/.ssh/known_hosts')

        Ssh.client = child

    @classmethod
    def command(cls, cmd, prompt=']#', silent=False):
        Ssh.client.buffer = ''
        Ssh.client.send(cmd + "\r")
        Ssh.client.expect(prompt)
        if not silent:
            print Ssh.client.before, Ssh.client.after,
        return Ssh.client.before, Ssh.client.after

    @classmethod
    def close(cls, ):
        Ssh.client.close()


@app.route('/')
def hello_world():
    return 'Hello World!'


def rtail():
    pass


if __name__ == '__main__':
    #app.run()
    rtail()
