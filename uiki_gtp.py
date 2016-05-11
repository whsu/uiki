import sys
import argparse
from uiki.player import Player
from omnomnom.atari_player import AtariPlayer
from gtp.gtp_player import GtpPlayer

parser = argparse.ArgumentParser(description="Start Uiki in GTP mode")
parser.add_argument('-p', '--player', default='uiki',
                    help='Name of computer player')
parser.add_argument('-n', '--numplayouts', type=int, default=1000,
                    help='Number of MCTS playouts.')
parser.add_argument('-c', '--numcaps', type=int, default=1,
                    help='Number of captures to win capture go.')
args = parser.parse_args()

if args.player.lower() == 'uiki':
    player = Player(playouts=args.numplayouts)
elif args.player.lower() == 'omnomnom':
    player = AtariPlayer(num_caps=args.numcaps, playouts=args.numplayouts)
else:
    raise ValueError('Unknown player {0}'.format(args.player))

gtp_player = GtpPlayer(player, sys.stdin, sys.stdout)
gtp_player.run()
