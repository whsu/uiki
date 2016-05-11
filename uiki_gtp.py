import sys
import argparse
from uiki.player import Player
from gtp.gtp_player import GtpPlayer

parser = argparse.ArgumentParser(description="Start Uiki in GTP mode")
parser.add_argument("-p", "--playouts", type=int, default=1000, help='Number of MCTS playouts.')
args = parser.parse_args()

p = Player(playouts=args.playouts)
gtp_player = GtpPlayer(p, sys.stdin, sys.stdout)
gtp_player.run()
