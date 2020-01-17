<template>
<div>


<h1 id="rCode" class="">Room code: {{ $route.params.code }} </h1>
<transition enter-active-class="animated fadeIn delay-1s" leave-active-class="animated fadeOut">
<h1 v-if="!playing">The lobby is open!</h1>
</transition>

<transition enter-active-class="animated fadeIn delay-1s" leave-active-class="animated fadeOut">
<h1 v-if="playing">The lobby is closed</h1>
</transition>

<br>
<transition enter-active-class="animated fadeIn delay-1s" leave-active-class="animated fadeOut">
  <h1 v-if="state==='V'"> {{question}} </h1>
</transition>


<br>

<!-- <h1 v-if="isHost === $route.params.username">You are the host</h1> -->
<transition enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
<h1 v-if="state==='V'">Users have answered: </h1>
<h1 v-if="state==='R'">Results: </h1>
<div v-if="state==='R'"  class="centered">

<div>
  <button class="card animated rollIn"  v-for="(user, index) in players" v-bind:key="user">
        <div class="top">
          {{ user }}
        </div>
        <div class="bottom">
          {{ points[index] }} points
          <div v-if="user===faker && caught===false">
            <br>
          Got away!
        </div>
        </div>


        <!-- endpoint for vote correct -->

  </button>


</div> 


</div>
</transition>
<br>
<div class="centered" v-if="state==='V'">
  <button class="card animated rollIn"  v-for="single_answer in answers" v-bind:key="single_answer">

        <div class="top">
          {{ single_answer.user_name }} said:
        </div>
        <div class="bottom">
          {{single_answer.answer}}
        </div>

        <div>
          <!--{{ votes(single_answer.user_name) }} votes -->
          <!-- API endpoint coming soon -->
        </div>

  </button>
</div>


</div>
</template>

<script>
import axios from 'axios'

export default {
  name: "spectator",
  data() {
    return {
      answers: [],
      state: "N",
      stateTimer: null,
      code: "",
      selected: "",
      buttonArray: [],
      animTimer: null,
      playing: false,
      votedArray: [],
      lastState: "N",
      got: false,
      question: "",
      qID:0,
      players: [],
      points: []
    }
  },
  methods: {
    getState() {
        let self = this


if(this.state === "V" && !this.got){
  axios.get("/api/rooms/" + self.$route.params.code + "/getanswers").then(function (result){
  //console.log(result.data)
    self.answers = result.data
    //console.log(typeof self.answers)
    self.got = true
  })
}

      if(this.state === "W"){
        this.got = false
        this.answers = []
      }

        

        axios.get("/api/rooms/" + self.$route.params.code).then(function (result){
              if(result.data.state === "W"){
                self.playing = false
                self.players = result.data.user_list
              }
              else{
                self.playing = true
              }
       })

       axios.get("/api/rooms/" + self.$route.params.code).then(function (result) {
          self.votedArray = result.data.voted_array
          self.points = result.data.user_points
          console.log(self.votedArray)
        })

        axios.get("/api/rooms/" + self.$route.params.code).then(function (result) {
          self.state = result.data.state
        }).catch(function (error) {
          self.showGetErr({message: error, title: "getSTate - voting"})
          return;
        })

        if(this.state === "D"){
          window.clearInterval(self.animTimer)
          window.clearInterval(self.stateTimer)

          this.showExitMsg()

          this.$router.push("/").catch(err => {
        //do nothing
      })
        }

        axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
                    self.qID = response.data.question_id
                    axios.get("/api/questions/" + self.qID + "/right").then(function (response){
                        self.question = response.data.prompt
                    })
        })
    },
    updateAnim(){
      //var item = items[Math.floor(Math.random()*items.length)];

      var anims = ["bounce", "flash", "pulse", "rubberBand", "rubberBand", "headShake", "swing", "tada", "wobble", "jello"]

      var chosen = anims[Math.floor(Math.random()*anims.length)]

      var page = document.getElementById("rCode")

      var classList = page.classList;
        while (classList.length > 0) {
        classList.remove(classList.item(0));
      }

      classList.add("animated", chosen);

      console.log("animated " + chosen)

    },
    votes(user){
      //console.log("running vote for: " user)
        var ret = 0

        var i;
        for (i = 0; i < this.votedArray.length; i++) {
          var vName = this.votedArray[i].split(",")

          if(user === vName){
            ret = ret + 1
          }

        }

      return ret
    }
  },
  computed: {

    voteCount(user){
        return 0
    }

  },
  asyncComputed: {
      isHost() {
        let self = this
        return(axios.get("/api/rooms/" + self.$route.params.code).then(response => response.data.host))
    }
  },
  created () {
  document.title = this.$route.params.code + " - Results"
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
    self.points = response.data.user_points
    self.players = response.data.user_list
   })

},
 mounted: function() {
            this.stateTimer = window.setInterval(() => {
                this.getState()
            }, 700)

            this.animTimer = window.setInterval(() => {
              if(!this.playing){
              this.updateAnim()
              }
            }, 5000)
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
      },
      showExitMsg: { 
        message: "This lobby has been closed!",
        type: 'info' 
      }
 }
}

</script>

<style scoped lang="scss">

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


@for $i from 1 through 10 {
    .card:nth-child(#{$i}n) {
        animation-delay: #{$i * 0.45}s;
    }
}



.container {
  padding: 2px 16px;
  

.centerContainer-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
}

</style>