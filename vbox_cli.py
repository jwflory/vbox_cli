#!/usr/bin/env python3
"""
Python CLI tool to perform basic VirtualBox processes tasks via `vboxmanage`

Authored by Justin W. Flory.

Wrapper program for the VirtualBox `vboxmanage` tool provided by Oracle. This
wrapper reduces complexity for common, frequent operations. As written, it
could be used for automation for basic VirtualBox operations and expanded if
needed.

This wrapper script was originally written for NSSA-244 Virtualization course
assignment at the Rochester Institute of Technology in Spring 2019. Prof.
Garret Arcoraci taught the course.

LICENSE: Mozilla Public License 2.0
"""

import argparse
import subprocess
import sys


def opt_create(args):
    """Create a new VirtualBox virtual machine with vboxmanage."""
    vbox_cmd_str = 'vboxmanage createvm --register --name ' \
        + args.vbox_vm_name

    if args.vbox_vm_groups is not None:
        vbox_cmd_str += ' --groups ' + args.vbox_vm_groups
    elif args.vbox_vm_os is not None:
        vbox_cmd_str += ' --ostype ' + args.vbox_vm_os

    subprocess.run(vbox_cmd_str.split(), check=True)


def opt_delete(args):
    """Delete an existing VirtualBox virtual machine with vboxmanage."""
    subprocess.run([
        'vboxmanage',
        'unregistervm',
        '--delete',
        args.vbox_vm_identifier],
        check=True)


def opt_info(args):
    """List all VirtualBox virtual machines or details from a specific one."""

    # Look up details for a specific VM
    if args.vbox_vm_identifier is not None:
        subprocess.run([
            'vboxmanage',
            'showvminfo',
            '--details',
            args.vbox_vm_identifier],
            check=True)

    # List all registered VMs
    else:
        subprocess.run([
            'vboxmanage',
            'list',
            'vms'],
            check=True)


def opt_status(args):
    """Start or stop an existing VirtualBox virtual machine."""

    # Start a headless VM
    if args.vbox_vm_action == 'start':
        subprocess.run([
            'vboxmanage',
            'startvm',
            args.vbox_vm_identifier,
            '--type',
            'headless'],
            check=True)

    # Stop a running VM
    elif args.vbox_vm_action == 'stop':
        subprocess.run([
            'vboxmanage',
            'controlvm',
            args.vbox_vm_identifier,
            'poweroff'],
            check=True)
    else:
        print('//TODO: proper error handling')


def main():
    """Main method to set up argument parsing."""

    # Set up argument parser and subparsers
    parser = argparse.ArgumentParser(
        description='Wrapper script to simplify basic VirtualBox tasks',
        epilog='Note: "VMs" refers to virtual machines')
    subparsers = parser.add_subparsers(
        help='sub-command help')

    # Parser for "create" sub-command
    parser_create = subparsers.add_parser(
        'create',
        help='create a new VirtualBox VM')
    parser_create.add_argument(
        '--name',
        dest='vbox_vm_name',
        help='(required) name of new VM',
        metavar='<vm_name>',
        required=True)
    parser_create.add_argument(
        '-g', '--groups',
        dest='vbox_vm_groups',
        help='optionally specify groups to assign to VM',
        metavar='<group>, ...')
    parser_create.add_argument(
        '-o', '--operating-system',
        dest='vbox_vm_os',
        help='optionally specify an operating system to use',
        metavar='<os_name>')

    # Parser for "delete" sub-command
    parser_delete = subparsers.add_parser(
        'delete',
        help='delete an existing VirtualBox VM')
    vm_delete_exclusive_args = \
        parser_delete.add_mutually_exclusive_group(required=True)
    vm_delete_exclusive_args.add_argument(
        '--name',
        dest='vbox_vm_identifier',
        help='name of VM to permanently delete',
        metavar='<vm_name>')
    vm_delete_exclusive_args.add_argument(
        '--uuid',
        dest='vbox_vm_identifier',
        help='UUID of VM to permanently delete',
        metavar='<vm_uuid>')

    # Parser for "info" sub-command
    parser_info = subparsers.add_parser(
        'info',
        help='list all VirtualBox VMs or get info about a specific VM')
    vm_info_exclusive_args = \
        parser_info.add_mutually_exclusive_group()
    vm_info_exclusive_args.add_argument(
        '--name',
        dest='vbox_vm_identifier',
        help='name of VM',
        metavar='<vm_name>')
    vm_info_exclusive_args.add_argument(
        '--uuid',
        dest='vbox_vm_identifier',
        help='UUID of VM',
        metavar='<vm_uuid>')

    # Parser for "status" sub-command
    parser_status = subparsers.add_parser(
        'status',
        help='start or stop a VM')
    vm_status_exclusive_args_ops = \
        parser_status.add_mutually_exclusive_group(required=True)
    vm_status_exclusive_args_ops.add_argument(
        '--start',
        action='store_const',
        const='start',
        dest='vbox_vm_action',
        help='start a specified VM')
    vm_status_exclusive_args_ops.add_argument(
        '--stop',
        action='store_const',
        const='stop',
        dest='vbox_vm_action',
        help='stop a specified VM')
    vm_status_exclusive_args_label = \
        parser_status.add_mutually_exclusive_group(required=True)
    vm_status_exclusive_args_label.add_argument(
        '--name',
        dest='vbox_vm_identifier',
        help='name of VM',
        metavar='<vm_name>')
    vm_status_exclusive_args_label.add_argument(
        '--uuid',
        dest='vbox_vm_identifier',
        help='UUID of VM',
        metavar='<vm_uuid>')

    # Actual processing of arguments and send to function
    args = parser.parse_args()
    if sys.argv[1] == 'create':
        opt_create(args)
    elif sys.argv[1] == 'delete':
        opt_delete(args)
    elif sys.argv[1] == 'info':
        opt_info(args)
    elif sys.argv[1] == 'status':
        opt_status(args)
    else:
        print('//TODO: proper error handling')


main()

# Resources used:
#   - https://docs.python.org/3.7/library/argparse.html
#   - https://docs.python.org/3.7/howto/argparse.html
#   - https://stackoverflow.com/a/8810797
#   - https://blog.scottlowe.org/2016/11/10/intro-to-vbox-cli/
#   - https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
#   - https://docs.python.org/3/library/subprocess.html
#   - https://docs.python.org/3.7/tutorial/datastructures.html
#   - https://stackoverflow.com/a/8113787
#   - https://www.python.org/dev/peps/pep-0257/
