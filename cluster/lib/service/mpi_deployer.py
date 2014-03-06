import ansible.playbook
from ansible import callbacks
from ansible import utils

class MpiDeployer():

    def __init__(self, configuration):
        self._config = configuration

    def deploy(self):
        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        inventory = ansible.inventory.Inventory(self._config.ansible_hosts_file)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats,
                                                      verbose=utils.VERBOSITY)
        pb = ansible.playbook.PlayBook(playbook=self._config.playbook,
                                       callbacks=playbook_cb,
                                       runner_callbacks=runner_cb,
                                       stats=stats, inventory=inventory)
        pb.run()
