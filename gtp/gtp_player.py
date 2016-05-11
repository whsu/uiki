from util.const import *

GTP_VERSION = '2'
GTP_PASS = 'pass'
GTP_RESIGN = 'resign'

def parse_command(line):
    '''Parse the GTP command.

    Parameters:
    - line : input line containing the GTP command.

    Returns:
    - cid : command ID, None if not provided.
    - command : GTP command, None if not provided.
    - arguments : list of arguments to the command, [] if not provided.
    '''
    i = line.find('#')
    if i >= 0:
        line = line[:i]

    fields = line.split()
    if len(fields) == 0:
        return (None, None, [])
    elif len(fields) == 1:
        return (None, fields[0], [])
    else:
        if fields[0].isdigit():
            return (fields[0], fields[1], fields[2:])
        else:
            return (None, fields[0], fields[1:])

def create_response(cid, message, error):
    '''Create the GTP response.

    Parameters:
    - cid : command ID, None if the command did not come with an ID.
    - message : result of the command or error message
    - error : whether the command results in error

    Returns:
    - response : string representing the GTP response.
    '''
    return '{}{}{}{}\n\n'.format('?' if error else '=',
                                 cid if cid is not None else '',
                                 ' ' if len(message)>0 else '',
                                 message)

def gtp_color(color_str):
    '''Get the color from a GTP command.'''
    color_str = color_str.lower()
    if color_str == 'w' or color_str == 'white':
        return WHITE
    elif color_str == 'b' or color_str == 'black':
        return BLACK
    else:
        raise ValueError('Invalid color {0}'.format(color_str))

def gtp_vertex(vertex_str):
    '''Get the vertex coordinate from a GTP command.'''
    if vertex_str.lower() == GTP_PASS:
        return GTP_PASS

    try:
        row = int(vertex_str[1:3])-1
        col = ord(vertex_str[0].lower())-ord('a')
        if col > ord('i')-ord('a'):
            col -= 1
        if 0 <= row < 25 and 0 <= col < 25:
            return (row, col)
        else:
            raise ValueError('Invalid vertex {0}'.format(vertex_str))
    except:
        raise ValueError('Invalid vertex {0}'.format(vertex_str))

def player_action_gtp(action):
    '''Converts player action to GTP vertex.'''
    if action == RESIGN:
        return GTP_RESIGN
    elif action == PASS:
        return GTP_PASS
    else:
        row, col = action
        if col >= ord('I')-ord('A'):
            col += 1
        return '{0}{1}'.format(chr(ord('A')+col), row+1)

class GtpPlayer:
    __commands__ = [
        'protocol_version',
        'name',
        'version',
        'known_command',
        'list_commands',
        'quit',
        'boardsize',
        'clear_board',
        'komi',
        'play',
        'genmove',
        'showboard',
    ]

    def __init__(self, player, fin, fout):
        self.player = player
        self.fin = fin
        self.fout = fout

    def run(self):
        while True:
            line = self.fin.readline()
            (cid, command, args) = parse_command(line)

            if command is None:
                continue

            error = False
            message = ''
            if command == 'protocol_version':
                message = GTP_VERSION
            elif command == 'name':
                message = self.player.__name__
            elif command == 'version':
                message = self.player.__version__
            elif command == 'known_command':
                message = 'true' if args[0] in self.__commands__ else 'false'
            elif command == 'list_commands':
                message = '\n'.join(sorted(self.__commands__))
            elif command == 'boardsize':
                try:
                    size = int(args[0])
                    if size <= 1 or size >= 26:
                        message = 'unacceptable size'
                        error = True
                    else:
                        self.player.new_game(rows=size, cols=size)
                except IndexError:
                    message = 'no boardsize received'
                    error = True
                except ValueError:
                    message = 'boardsize not an int'
                    error = True
            elif command == 'clear_board':
                self.player.reset_game()
            elif command == 'komi':
                try:
                    k = float(args[0])
                    self.player.set_komi(k)
                except IndexError:
                    message = 'no komi received'
                    error = True
                except ValueError:
                    message = 'komi not a float'
                    error = True
            elif command == 'play':
                try:
                    color = gtp_color(args[0])
                    vertex = gtp_vertex(args[1])
                    if vertex == GTP_PASS:
                        self.player.place_pass(color)
                    else:
                        row, col = vertex
                        legal = self.player.place_move(color, row, col)
                        if not legal:
                            message = 'illegal move'
                            error = True
                except:
                    message = 'invalid move'
                    error = True
            elif command == 'genmove':
                try:
                    color = gtp_color(args[0])
                    move = self.player.gen_move(color)
                    message = player_action_gtp(move)
                except:
                    message = 'invalid color'
                    error = True
            elif command == 'showboard':
                message = '\n' + self.player.show_board()
            elif command not in self.__commands__:
                message = 'unknown command'
                error = True

            response = create_response(cid, message, error)

            self.fout.write(response)
            self.fout.flush()

            if command == 'quit':
                break
