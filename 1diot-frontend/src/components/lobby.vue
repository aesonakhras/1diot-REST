<template>
<div>
  <div class="room-info">
    <h1 v-if="isHost === $route.params.username">You are the host</h1>
    <div class="code-info">
      <h1 class = "room-text">Code: </h1>
      <br>
      <h1 class="room-code">{{ $route.params.code }} </h1>
    </div>
    <h1 style="font-size: 1.25rem;">Players in the room:</h1>
  </div>

    <div class = "centerContainer" v-for="play in players" v-bind:key="play">
      <div v-if="play === $route.params.username" class="user-tag player">
        {{ play }}
      </div>
      <div v-else class="user-tag other">
        {{ play }}
      </div>

  </div>

<div class="centerContainer">
  <br>
  <br>
  <button class = "glow-on-hover" v-if="isHost === $route.params.username" v-on:click="gotoGame">Everyone is in!</button>

  <button class = "glow-on-hover" v-on:click="leaveGame">Leave Game</button>

  <button class = "glow-on-hover" v-if="isHost === $route.params.username" v-on:click="endGame">Close Lobby</button>
</div>


</div>
</template>

<script>

import axios from 'axios'

export default {
    name: "lobby",
    data() {
     return {
      players: [],
      state: "W",
      playerReady: "W",
      host: "",
      updateTimer: null
    }
  },
  methods: {
      lobbyPlayers() {
      let self = this
      axios.get("/api/rooms/" + self.$route.params.code).then(function (result){
      self.players = result.data.user_list
    }).catch(function (error) {
          self.showGetErr({message: error, title: "lobbyPlayers"})
          return;
    })
    },
    testGet: function (event) {
      let self = this
      if (event) {
        axios.get("/api/rooms/" + self.$route.params.code + "/getanswers").then(function (result){
          console.log("Getting answers")
          console.log(result.data[0].user_name)
        }).catch(function (error) {
          self.showGetErr({message: error, title: "testGet"})
          return;
    })
      }
    },
    switchGame() {
      console.log("Game switch!")
      window.clearInterval(self.updateTimer)
      this.$router.push("/game/" + this.$route.params.code + "/" + this.$route.params.username).catch(err => {
        //do nothing
      })
    },
    gotoGame: function (){
      let self = this
      if (event) {
        if(this.players.length <= 2){
          this.showNumErr()
          return;
        }
        else{
        window.clearInterval(self.updateTimer)
        //console.log("gotoGame")
        //console.log("get new Q")
        axios.post("/api/rooms/" + self.$route.params.code + "/setnewquestion", {}).then(function(){
          axios.post("/api/rooms/" + self.$route.params.code + "/setwronguser", {}).then(function(){
  axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "A"}).then(function (result) {
            axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "A"})
            axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "A"})
            self.switchGame()
          }).catch(function (error) {
            self.showGetErr({message: error, title: "gotoGame"})
            return;
        })
          })
        })
        //console.log("setBadPlayer!")
        //console.log(self)
        
        //console.log("switch game!")
        
      }
      }
    },
    isGame: function (){
      let self = this
      console.log("getting game state")
      axios.get("/api/rooms/" + self.$route.params.code).then(function (result) {
        self.state = result.data.state
        //console.log(self.state)
        //console.log(result.data.state)
      }).catch(function (error) {
          self.showGetErr({message: error, title: "isGame"})
          return;
      })
      if (this.state === "A") {
        console.log("isGame")
        window.clearInterval(self.updateTimer)
        this.switchGame()
      }
      else if (this.state === "D") {
        window.clearInterval(self.updateTimer)
        axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).catch(function (error) {
          self.showGetErr({message: error, title: "isGame"})
          return;
        })
        if(this.host === this.$route.params.username) {
          self.endGameNoMouse()
        }
        this.$router.push("/").catch(err => {
        //do nothing
      })
      }
    },
    leaveGame: function (event){
      let self = this
      if (event) {
          if(this.host === this.$route.params.username) {
            self.endGameNoMouse()
        }
        else {
        window.clearInterval(self.updateTimer)
        axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).catch(function (error) {
          self.showGetErr({message: error, title: "leaveGame - lobby"})
          return;
        })
        this.$router.push("/").catch(err => {
        //do nothing
      })
        }
      }
    },
    endGame: function (event){
      let self = this
      if (event) {
        window.clearInterval(self.updateTimer)
        axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "D"}).then(function (result) {
          axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).then(function (){self.$router.push("/").catch(err => {
        //do nothing
      })}).catch(function (error) {
            self.showGetErr({message: error, title: "endGame - lobby"})
          return;
        })
        }).catch(function (error) {
          self.showGetErr({message: error, title: "endGame - lobby"})
          return;
        })
        
      }
    },
    endGameNoMouse() {
        let self = this
        axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "D"}).then(function (result) {
          window.clearInterval(self.updateTimer)
          axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).then(function (){self.$router.push("/").catch(err => {
        //do nothing
      })}).catch(function (error) {
            self.showGetErr({message: error, title: "endGameNoMouse - lobby"})
          return;
        })
        }).catch(function (error) {
          self.showGetErr({message: error, title: "endGameNoMouse - lobby"})
          return;
        })
    }
  },
    asyncComputed: {
      isHost() {
        let self = this
        return(axios.get("/api/rooms/" + self.$route.params.code).then(response => response.data.host))
    }
  },
  created () {
    let self = this
    axios.get("/api/rooms/" + self.$route.params.code).then(function (result){
      console.log(result.data.user_list)
      self.players = result.data.user_list
    }).catch(function (error) {
          self.showGetErr({message: error, title: "created - lobby"})
          return;
    })

    axios.get("/api/rooms/" + self.$route.params.code).then(function (response) {
      self.host = response.data.host
    }).catch(function (error) {
          self.showGetErr({message: error, title: "created - lobby"})
          return;
    })

    axios.get("/api/rooms/" + self.$route.params.code).then(function (result) {
      console.log("Got State")
      self.state = result.data.state
    }).catch(function (error) {
          self.showGetErr({message: error, title: "created - lobby"})
          return;
    })

    document.title = this.$route.params.code + " - Lobby"

    this.playerReady = "W"

  },
  mounted: function () {
      this.updateTimer = window.setInterval(() => {
         this.lobbyPlayers()
         if(this.host != this.$route.params.username){
          this.isGame()
         }
  }, 3000)
  },
  notifications: {
      showGetErr: { 
        title: 'Request Error',
        message: 'Issue goes here',
        type: 'error' 
      },
      showNumErr: { 
        title: 'Too Few Players',
        message: 'You need at least three users to start a game!',
        type: 'error' 
      }
    },

}

</script>

<style scoped>

.room-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.code-info {
  display: flex;
  flex-direction: column;
  align-content: flex-start;
  margin: 0px;
}

.room-text {
  font-size: 1rem;
  padding: 0px;
}

.room-code {
  color: #6EB4EC;
  margin: 0px; 
  font-size: 4.0rem;
  padding: 0px;
  margin-top: -20px;
}

body {
  background: rgb(20,20,20);
}

h1 {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    padding-bottom: 10px;
    margin: 0px;
}


.user-tag {

  border-radius: 10px;
  width: 300px;
  height: 40px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2.0rem;
}

.player {
  background: #6EB4EC;
  background: -moz-linear-gradient(-45deg, #6EB4EC 0%, #6bb667 100%);
  background: -webkit-linear-gradient(-45deg, #6EB4EC 0%, #6bb667 100%);
  background: linear-gradient(135deg, #6EB4EC 0%, #6bb667 100%);
}

.other {
  background: #D0CDCD;
  background: -moz-linear-gradient(-45deg, #D0CDCD 0%, #848282 100%);
  background: -webkit-linear-gradient(-45deg, #D0CDCD 0%, #848282 100%);
  background: linear-gradient(135deg, #D0CDCD 0%, #848282 100%);
}

.centerContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.glow-on-hover {
    width: 300px;
    height: 50px;
    border: 1px solid #6EB4EC;
    padding: 3px 0px 3px 3px;
    margin: 5px 1px 3px 0px;
    outline: none;
    color: #fff;
    background: rgb(20,20,20);
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 10px;
    font-size: 1.5rem;
}

.glow-on-hover:hover  {
  box-shadow: 0 0 5px #6EB4EC;
  transition: 0.3s;
  border-radius: 10px;
}

.glow-on-hover:focus  {
  box-shadow: 0 0 5px #6EB4EC;
  transition: 0.3s;
  border-radius: 10px;
}



</style>