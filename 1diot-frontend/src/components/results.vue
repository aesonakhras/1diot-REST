<template>
<div>
<transition enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
  <div class="centerContainer" v-if="time > 2 && time < 6"><h1>{{ faker }} was the odd one out!</h1></div>
</transition>

<transition>
<div v-show="time > 6">
<div class="centerContainer-list">
  <button class="card animated rollIn"  v-for="(user, index) in answers" v-bind:key="user">
        <div class="top">
          {{ user.user_name }}
        </div>
        <div class="bottom">
          {{ points[index] }} points
          <div v-if="(user==faker) && (caught===false)">
            <br>
          Got away!
        </div>
        {{user.user_selected}}
        </div>


        <!-- endpoint for vote correct -->

  </button>

</div>
</div> 

  <div class="centered">
    <br>
    <div class="centerContainer-buttons">
    <br>
    <button class="glow-on-hover" v-if="host === $route.params.username" v-on:click="lobbyMouse">Play Again!</button>
    <br>
    <button class="glow-on-hover" v-if="host === $route.params.username" v-on:click="endMouse">Close Lobby</button>
  </div>
</div>




</transition>

</div>
</template>

<script>
import axios from 'axios'

  export default {
    name: "results",
    data() {
     return {
      players: [],
      state: "R",
      host: "",
      stateTimer: null,
      votes: [],
      intro: false,
      faker: "",
      caught: null,
      voteCount: 0,
      points: [],
      introTimer: null,
      time: 0,
      answers: []
    }
  },
  methods: {
    getState(){
      let self = this
      console.log("got state")
      console.log("who is caught:" + self.caught)
      console.log(this.state)
      axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
        self.state = response.data.state
        self.caught = response.data.caught
        self.points = response.data.user_points
      }).catch(function (error) {
        self.showGetErr({message: error, title: "getState error"})
        return;
      })
       
      if(this.state === "W"){
          console.log("lobby time")
          this.gotoLobby()
        }
        else if(this.state === "D"){
          this.leaveGame()
        }

    },
    introUpdate(){
      this.time = this.time + 1
      if(this.time > 10){
        window.clearInterval(this.introTimer)
      }
    },
    endMouse: function(event){
      if (event){
        this.endGame()
      }
    },
    lobbyMouse: function(event){
      if (event){
        console.log("clicked")
        this.gotoLobby()
      }
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
    gotoLobby(){
      console.log("going lobby")
      let self = this
      window.clearInterval(self.stateTimer) //kill timer
      //RESET ROOM
      axios.post("/api/rooms/" + self.$route.params.code + "/clearroom", {})
      //go to lobby
      axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "W"})
      axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "W"})
      axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "W"})
      this.$router.push("/lobby/" + self.$route.params.code + "/" + self.$route.params.username).catch(err => {
        //do nothing
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
    }

  },
  mounted: function () {
      this.stateTimer = window.setInterval(() => {
         this.getState()
      }, 500)

      this.introTimer = window.setInterval(() => {
        this.introUpdate()
      }, 1000)
  },
  created() {
      //initialize
      let self = this
        axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
        self.faker = response.data.user_wrong
        self.caught = response.data.caught
        self.voteCount = response.data.vote_count
        self.votes = response.data.voted_array
        self.points = response.data.user_points
        self.players = response.data.user_list
        self.host = response.data.host
      })

      axios.get("/api/rooms/" + self.$route.params.code + "/getanswers").then(function (result){
  console.log(result.data)
    self.answers = result.data
    console.log(typeof self.answers)
  })
  },
  asyncComputed: {
      isCaught() {
        let self = this
        axios.get("/api/rooms/" + self.$route.params.code).then(function(response){
          console.log("get caught resp:\n")
          console.log(response)
          return response.data.caught
        })
      }
  },
  notifications: {
            showGetErr: { 
                title: 'Request Error',
                message: 'Issue goes here',
                type: 'error' 
            }
  }

  }

</script>

<style scoped lang="scss" >

h1 {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin: 0px;
    padding: 0px;
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

.centerContainer-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.centerContainer {
  display: flex;
  flex-direction: row;
  position: absolute;
  top: 50%; 
  right: 50%;
  transform: translate(50%,-50%);
  font-size: 2rem;
}

@media (min-width: 780px) {
    .centerContainer {
        font-size: 11px;
    }
}

@media (min-width: 702px) {
    .centerContainer {
        font-size: 10px;
    }
}

@media (min-width: 724px) {
    .centerContainer {
        font-size: 9px;
    }
}

@media (max-width: 623px) {
    .centerContainer {
        font-size: 8px;
    }
}

@media (min-width: 1000px) {
    .centerContainer {
        font-size: 20px;
    }
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

.centerContainer-buttons {
  display: flex;
  flex-direction: column;
  // top: 50%; 
  // right: 50%;
  // transform: translate(50%,-50%);
  font-size: 2rem;
  padding: 0px;
  margin: 0px;
}

</style>