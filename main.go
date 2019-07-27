package main

import (
	// "flag"
	"fmt"
	"os"
	"os/signal"
	"syscall"
  "strings"
	"github.com/bwmarrin/discordgo"
  "github.com/joho/godotenv"
  // "net/http"

)

// Variables used for command line parameters
var (
  Token  string 
)
func init() {

	// flag.StringVar(&Token, "t", "", "Bot Token")
	// flag.Parse()
}
func main() {
  fmt.Println("Started!")
    err := godotenv.Load()
  if err != nil {
    log.Fatal("Error loading .env file")
  }
  Token = os.Getenv('TOKEN')

	// Create a new Discord session using the provided bot token.
	dg, err := discordgo.New("Bot " + Token)
	if err != nil {
		fmt.Println("error creating discord session,", err)
		return
	}

	// Register the messageCreate func as a callback for MessageCreate events.
	dg.AddHandler(messageCreate)

	// Open a websocket connection to Discord and begin listening.
	err = dg.Open()
	if err != nil {
		fmt.Println("error opening connection,", err)
		return
	}

	// Wait here until CTRL-C or other term signal is received.
	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-sc

	// Cleanly close down the Discord session.
	dg.Close()
  // http.HandleFunc("/", HelloServer)
  //   http.ListenAndServe(":8080", nil)
}

// This function will be called (due to AddHandler above) every time a new
// message is created on any channel that the autenticated bot has access to.
func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {

	// Ignore all messages created by the bot itself
	// This isn't required in this specific example but it's a good practice.
	if m.Author.ID == s.State.User.ID {
		return
	}
	// If the message is "ping" reply with "Pong!"
  // commands := [5]string{"ping","pong"}
  prefix := "./"
  
  if strings.HasPrefix(m.Content, prefix) {
    _cmd := strings.Split(m.Content, " ")
    cmd  := _cmd[0]
    args := _cmd
    _args:= strings.Join(args, ", ")
    if(cmd == prefix + "ping"){
      s.ChannelMessageSend(m.ChannelID, _args)
    }
//     if(cmd == prefix + "setchannel"){
//         s.ChannelMessageSend(m.ChannelID, string(args[1]))

//     }
    if(cmd == prefix + "down"){
      s.ChannelMessageSend(m.ChannelID, "Alright, sent an alert to Zane and Nebulium.")
      s.ChannelMessageSend("604047206042959895", "[<@261786467288875010> <@505881403175731210>] <@" + m.Author.ID + "> Reports that the server is down, (see <#602741527965597698>)\n\nTo reboot: `screen -r mc`, CTRL + C, then `bash run.sh`")
    }
  }
  
  
// 	if m.Content == "ping" {
// 		s.ChannelMessageSend(m.ChannelID, "Pong!")
// 	}

// 	// If the message is "pong" reply with "Ping!"
// 	if m.Content == "pong" {
// 		s.ChannelMessageSend(m.ChannelID, "Ping!")
// 	}
}
