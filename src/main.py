from bot import TheHabbitBot

def main():
    # TODO: TheHabbitBot class with destructor for closing all of the fds
    # app.post_shutdown()
    bot = TheHabbitBot()
    bot.run()

if __name__ == "__main__":
    main()
