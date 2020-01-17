<template>
<div>
<!-- <h1>Room code: {{ $route.params.code }} </h1> -->
<!-- <h1>You are: {{ $route.params.username }}</h1> -->
<!-- <h1 v-if="isHost === $route.params.username">You are the host</h1> -->
<div v-if="voted == false"> 
  <h1>There are {{votes}} votes for you</h1>
  <h1>Users have answered: </h1>
  <div class="centered">
    <button class="card animated rollIn" v-for="single_answer in answers" v-bind:key="single_answer" v-on:click="makeVote(single_answer.user_name)" :disabled="voted == true">
          <div class="top">
            {{ single_answer.user_name }} said:
          </div>
          <div class="bottom">
            {{single_answer.answer}}
            <br>

          </div>
    </button>
  </div>
  <br>
  <div class="centerContainer">
    <button class="glow-on-hover" v-on:click="lock" :disabled="voted == true">Lock in vote</button>
  </div>
</div>
<div v-else-if="voted==true">
  <div class="centered already-voted">
    You have voted!
  </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: "voting",
  data() {
    return {
      answers: [],
      state: "V",
      stateTimer: null,
      code: "",
      selected: "",
      voted: false,
      host: "",
      advance: false,
      votes: 0
    }
  },
  methods: {
    getState() {
        let self = this
        axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
          self.advance = response.data.winner_determined
        })
        //console.log(this.state)
        axios.get("/api/rooms/" + self.$route.params.code).then(function (result) {
          self.state = result.data.state
        }).catch(function (error) {
          self.showGetErr({message: error, title: "getState - voting"})
          return;
        })
        if(this.state === "R"){
          console.log("res")
          this.gotoRes()
        }
        else if(this.state === "D"){
          this.leaveGame()
        }

        axios.post("/api/rooms/" + self.$route.params.code + "/uservotes", {user_name: self.$route.params.username}).then(function (result){
        self.votes = result.data.votes
      })
    },
    leaveGame(){
      let self = this
      window.clearInterval(self.stateTimer) //kill timer
      axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).catch(function (error) {
          self.showGetErr({message: error, title: "leaveGame - voting"})
          return;
        })
        //go to index
        this.$router.push("/").catch(err => {
        //do nothing
      })
    },
    gotoRes(){
      console.log("going res")
      let self = this
      window.clearInterval(self.stateTimer) //kill timer
      //RESET ROOM
      //axios.post("/api/rooms/" + self.$route.params.code + "/clearroom", {})
      //go to results
      if(self.host === self.$route.params.username){
        axios.post("/api/rooms/" + self.$route.params.code + "/determinewinner", {})
      }

        axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "R"}).then(function(response) {
          axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "R"})
          axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "R"})
          console.log("determine winner resp:\n")
          console.log(response)
        }).then(
      self.$router.push("/results/" + self.$route.params.code + "/" + self.$route.params.username).catch(err => {
        //do nothing
      }))
    },
    endGame(){
      let self = this
        axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "D"}).then(function (result) {
          axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "D"})
          axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "D"})
          window.clearInterval(self.stateTimer)
          axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).then(function (){self.$router.push("/").catch(err => {
        //do nothing
      })}).catch(function (error) {
            self.showGetErr({message: error, title: "endGame - voting"})
          return;
        })
        }).catch(function (error) {
          self.showGetErr({message: error, title: "endGame - voting"})
          return;
        })
    },
    endMouse: function(event){
      if (event){
        this.endGame()
      }
    },
    lobbyMouse: function(event){
      if (event){
        this.gotoLobby()
      }
    },
    makeVote(voted) {
      let self = this
      this.selected = voted
      if (voted === this.$route.params.username){
        this.showVoteErr()
        this.selected = voted
      }
      else{
        axios.post("/api/rooms/" + self.$route.params.code + "/vote", {user_name: self.$route.params.username, user_selected: self.selected, locked: false})
      }
    },
    lock: function (event){
      let self = this
      if(event){
        if(this.selected != this.$route.params.username){
          axios.post("/api/rooms/" + self.$route.params.code + "/vote", {user_name: self.$route.params.username, user_selected: self.selected, locked: true})
          this.voted = true
        }
        else{
          this.showVoteErr()
        }
      }
    },
    votesBAD(user) {
      let self = this
      axios.post("/api/rooms/" + self.$route.params.code + "/uservotes", {user_name: user}).then(function (result){
        return result.data.votes
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
  document.title = this.$route.params.code + " - Voting"
  let self = this
  axios.get("/api/rooms/" + self.$route.params.code + "/getanswers").then(function (result){
  console.log(result.data)
    self.answers = result.data
    console.log(typeof self.answers)
  }).catch(function (error) {
      self.showGetErr({message: error, title: "created - voting"})
      return;
  })
   axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
    self.code = response.data.room_code
   })
   axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
    self.host = response.data.host
   })
},
 mounted: function() {
            this.stateTimer = window.setInterval(() => {
                this.getState()
            }, 1000)
 },
 notifications: {
      showGetErr: { 
        title: 'Request Error',
        message: 'Issue goes here',
        type: 'error' 
      },
      showVoteErr: { 
        message: "You can't vote for yourself!",
        type: 'error' 
      }
 }
}

</script>

<style lang="scss" scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.7.2";
body {
  background: rgb(20,20,20);
}

h1 {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.centered {
  display: flex;
  flex-wrap: wrap;
  justify-content:space-evenly;
  align-content: space-around;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem; 
}

.centerContainer {
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  outline: none;
  box-shadow: 0 0 20px rgba(81, 203, 238, 1);
  transition: 0.3s;
  //border-radius: 10px;
  background-color: white;
  color: rgb(20,20,20);
  min-height: 100px;
  min-width: 300px;
  max-height: 120px;
  max-width: 300px;
  margin-bottom: 30px;
  margin-right: 15px;
  margin-left: 15px;
  -webkit-user-select: none; /* Safari */        
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
  font-size: 20px;
  position:relative;
  border: 0px;
  border-radius: 10px;
  padding: 0px;

  .top {
    transition: 0.3s;
    font-size:30px;
    height:35px;
    width: 300px;
    border-radius: 10px 10px 0px 0px;
    background: #6EB4EC;
    background: -moz-linear-gradient(-45deg, #6EB4EC 0%, #6bb667 100%);
    background: -webkit-linear-gradient(-45deg, #6EB4EC 0%, #6bb667 100%);
    background: linear-gradient(135deg, #6EB4EC 0%, #6bb667 100%); 
    color: white;
    margin-top: -2px;
    padding-bottom: 5px;
  }

  .bottom {
    transition: 0.3s;
    height:85px;
    margin: auto;
    text-align: center;
    padding-top: 5px;
    padding-left: 5%;
    padding-right: 5%;
    font-size:1rem;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}


.card:focus  {
  box-shadow: 0 0 20px rgba(255,0, 0, 1);
  transition: 0.3s;
  border-radius: 10px;
  .top {
    transition: 0.3s;
    background: #D7009D;
    background: -moz-linear-gradient(-45deg, #D7009D 0%, #E30000 100%);
    background: -webkit-linear-gradient(-45deg, #D7009D 0%, #E30000 100%);
    background: linear-gradient(135deg, #D7009D 0%, #E30000 100%);
  }
}




.card:hover  {

  box-shadow: 0 0 20px rgba(255,0, 0, 1);
  transition: 0.3s;
  border-radius: 10px;

  .top {
    transition: 0.3s;
    background: #D7009D;
    background: -moz-linear-gradient(-45deg, #D7009D 0%, #E30000 100%);
    background: -webkit-linear-gradient(-45deg, #D7009D 0%, #E30000 100%);
    background: linear-gradient(135deg, #D7009D 0%, #E30000 100%);
  }
}

@for $i from 1 through 10 {
    .card:nth-child(#{$i}n) {
        animation-delay: #{$i * 0.45}s;
    }
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

.container {
  padding: 2px 16px;
  
}

.already-voted {
  font-size: 2rem;
}

</style>