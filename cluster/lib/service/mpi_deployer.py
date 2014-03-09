import ansible.playbook
from ansible import callbacks
from ansible import utils

class MpiDeployer():
    """
    Deploys MPI environment to nodes using ansible api.
    Works similar to ansible-playbook command.
    """
    
    def __init__(self, configuration):
        """
        Creates new instance of MpiDeployer."

        :param configuration: Configuration with path to ansible playbook.
        """
        self._config = configuration

    def deploy(self):
        """
        Runs ansible playbook.
        """
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
