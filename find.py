#!/usr/bin/python

from __future__ import print_function
import sys
from bugzilla import Bugzilla
from bugzilla.bug import Bug
from prettytable import PrettyTable
from textwrap import TextWrapper


bz = Bugzilla('bugzilla.redhat.com')
if not bz.logged_in:
    print('please log in with the `bugzilla login` command')
    raise SystemExit(1)

PRODUCT = 'Red Hat Ceph Storage'
try:
    RELEASE = sys.argv[1]
except IndexError:
    RELEASE = '3.0'


def query_params(target_release=None):
    """ Return a dict of basic Bugzilla search parameters. """
    params = {
        'include_fields': ['id', 'summary', 'status'],
        'f1': 'product',
        'o1': 'equals',
        'v1': PRODUCT,
    }
    if target_release:
        params.update({
            'f2': 'target_release',
            'o2': 'equals',
            'v2': target_release,
        })
    return params.copy()


def search(payload):
    """
    Send a payload to the Bug.search RPC, and translate the result into
    bugzilla.bug.Bug results.
    """
    result = bz._proxy.Bug.search(payload)
    bugs = [Bug(bz, dict=r) for r in result['bugs']]
    return bugs


def find_future_features():
    """ Find all verified bugs with FutureFeature keyword """
    payload = query_params(RELEASE)
    payload.update({
        'f3': 'bug_status',
        'o3': 'equals',
        'v3': 'VERIFIED',
        'f4': 'keywords',
        'o4': 'allwordssubstr',
        'v4': 'FutureFeature',
    })
    return search(payload)


def find_customer_cases():
    """ Find all verified bugs with a customer case attached """
    payload = query_params(RELEASE)
    payload.update({
        'f3': 'bug_status',
        'o3': 'equals',
        'v3': 'VERIFIED',
        'f4': 'external_bugzilla.description',
        'o4': 'equals',
        'v4': 'Red Hat Customer Portal',
    })
    return search(payload)


def find_fixed_known_issues():
    """ Find all verified bugs marked as "Known Issue"  """
    payload = query_params(RELEASE)
    payload.update({
        'f3': 'bug_status',
        'o3': 'equals',
        'v3': 'VERIFIED',
        'f4': 'cf_doc_type',
        'o4': 'equals',
        'v4': 'Known Issue',
    })
    return search(payload)


def find_remaining_known_issues():
    """ Find all newer bugs marked as "Known Issue"  """
    # XXX TODO
    raise NotImplementedError('How would we define these?')


def print_report(bugs):
    """ Print a PrettyTable report of bug URLs and summaries """
    urls = []
    summaries = []
    x = PrettyTable()
    wrapper = TextWrapper(subsequent_indent='  ', width=36)
    for bug in bugs:
        urls.append('https://bugzilla.redhat.com/%s' % bug.id)
        summary = "\n".join(wrapper.wrap(bug.summary))
        summaries.append(summary)
    x.add_column("url", urls)
    x.add_column("summary", summaries)
    x.align = 'l'
    print(x)


bugs = find_future_features()
print('RFEs: %d' % len(bugs))
print_report(bugs)

bugs = find_customer_cases()
print('Customer Cases: %d' % len(bugs))
print_report(bugs)

bugs = find_fixed_known_issues()
print('Fixed Known Issues: %d' % len(bugs))
print_report(bugs)
