import ansible.runner
import ansible.playbook
from ansible import callbacks
from ansible import utils
from passlib.hash import sha512_crypt

class TowerApiCallbacks(callbacks.PlaybookCallbacks):
  def on_stats(self, stats):
    # TO-DO: check that everything worked well or not
    pass

class TowerApiRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):
  def on_failed(self, host, res, ignore_errors=False):
    # TO-DO: add corresponding error handler and notify
    super(TowerApiRunnerCallbacks, self).on_failed(host, res, ignore_errors=ignore_errors)

  def on_unreachable(self, host, res):
    # TO-DO: add corresponding error handler and notify
    if type(res) == dict:
      res = res.get('msg','')
    super(TowerApiRunnerCallbacks, self).on_unreachable(host, res)

  def on_async_failed(self, host, res, jid):
    # TO-DO: add corresponding error handler and notify
    super(TowerApiRunnerCallbacks, self).on_async_failed(host,res,jid)

class TowerApi(object):
  def run(self, data, remote_address):

    action = data['action'][0]
    is_allowed = self.allowed_requestor(action, remote_address)
    if not is_allowed:
      return False

    if action == 'setup_sandbox':
      if not ('nickname' in data and 'job_id' in data and 'repo_name' in data and 'password' in data):
        return False
      ret = self.run_playbook(action, {
        'nickname': data['nickname'][0],
        'job_id': data['job_id'][0],
        'repo_name': data['repo_name'][0],
        'crypted_pass': sha512_crypt.encrypt(data['password'][0])
      })
      return ret

    #elif data['action'] == 'other_method':
      # do something


  def allowed_requestor(self, api_action, remote_address):
    return True

  def run_playbook(self, name, extra_vars):
    stats = callbacks.AggregateStats()
    playbook_cb = TowerApiCallbacks(verbose=utils.VERBOSITY)
    runner_cb = TowerApiRunnerCallbacks(stats, verbose=utils.VERBOSITY)
    playbook_path = 'playbooks/' +  name + '/main.yml';
    inventory_path = 'playbooks/' + name + '/hosts';
    pb = ansible.playbook.PlayBook(
      playbook=playbook_path,
      stats=stats,
      callbacks=playbook_cb,
      inventory=ansible.inventory.Inventory(inventory_path),
      runner_callbacks=runner_cb,
      extra_vars=extra_vars
    )
    return pb.run()
