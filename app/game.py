class Game:
    
    def on_init(self):
        pass

    def on_execute(self):
        self.on_init()


if __name__ == "__main__" :
    theGame = Game()
    theGame.on_execute()