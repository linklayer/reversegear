=======================================================================
ReverseGear: Offline Reverse Engineering Tools for Automotive Networks
=======================================================================

Installation
------------

ReverseGear can be installed with pip: ``pip3 install reversegear``.

Rationale
---------

A variety of techniques exist for reverse engineering components by analyzing vehicle logs. ReverseGear aims to provide tools for automating these techniques. It is only intended for working offline, using logs of network traffic. For an online tool, see `caringcaraboo`_.

.. _caringcaraboo https://github.com/CaringCaribou/caringcaribou

Inputs
------
Currently, only :code:`candump` format logs files are supported. To generate a log using :code:`candump`, the :code:`-l` (or :code:`-L`) flag **must** be used.

For example, to log from the can0 interface:

:code:`candump -l can0`

Commands
--------

ReverseGear uses a number of subcommands. In general, you can get help with :code:`reversegear --help`, and :code:`reversegear [subcommand] --help`.

ids
...

Subcommand for generating arbitration ID statistics.

Usage: :code:`reversegear uds [-h] tx_id rx_id inputs [inputs ...]`

Example: :code:`reversegear ids log.txt`

uds
...

Subcommand for decoding Unified Diagnostic Services (ISO14229) traffic. Requires the arbitration ID transmitted by the client/scan tool (tx_id) and the arbitration ID received by the client/scan tool (rx_id).

Usage: :code:`reversegear uds [-h] tx_id rx_id inputs [inputs ...]`

Example: :code:`reversegear uds 0x7F1 0x7F9 log.txt`

iddiff
......

Subcommand for displaying unique arbitration IDs in two files.

Usage: :code:`reversegear iddiff [-h] a b`

Example :code:`reversegear iddiff log_one.txt log_two.txt`

