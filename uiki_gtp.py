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
parser.add_argument('-s', '--size', type=int, default=19,
                    help='Board size.')
parser.add_argument('-k', '--komi', type=float, default=6.5,
                    help='Komi.')
args = parser.parse_args()

if args.player.lower() == 'uiki':
    player = Player(playouts=args.numplayouts)
    player.new_game(rows=args.size, cols=args.size, komi=args.size)
elif args.player.lower() == 'omnomnom':
    player = AtariPlayer(playouts=args.numplayouts)
    player.new_game(rows=args.size, cols=args.size, num_caps=args.numcaps, komi=args.size)
else:
    raise ValueError('Unknown player {0}'.format(args.player))

gtp_player = GtpPlayer(player, sys.stdin, sys.stdout)
gtp_player.run()
