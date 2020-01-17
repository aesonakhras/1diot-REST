<template>
<div>
  <div class="logoContainer">
  <div>
      <h1 class="animated jackInTheBox">1DIOT</h1>
  </div>
  </div>


<div class="animated bounceInUp">
  <transition leave-active-class="animated bounceOutDown">
  <div class="inputContainer" v-if="!selected">
      <button class="glow-on-hover" v-on:click="initialRoom">Join a Room</button>
    </div>
  </transition>
</div>
<br>
<div class="animated bounceInUp">
  <transition leave-active-class="animated bounceOutDown">
  <div class="inputContainer" v-if="!selected">
      <button class="glow-on-hover" v-on:click="initialCreate">Create a Room</button>
    </div>
  </transition>
</div>
<br>
<div class="animated bounceInUp">
  <transition leave-active-class="animated bounceOutDown">
  <div class="inputContainer" v-if="!selected">
      <button class="glow-on-hover" v-on:click="initialView">View a Room</button>
    </div>
  </transition>
</div>

<transition enter-active-class="animated flipInX delay-1s" leave-active-class="animated flipOutX">

<div class="inputContainer" v-if="type==='join' || type=='create'">
  <div class="input">
      <input type="email" placeholder="Room Code" v-model="code" maxlength="4" autocomplete = "off" autocapitalize="none"> 
  </div>
</div>

</transition>

<transition enter-active-class="animated flipInX delay-1s" leave-active-class="animated flipOutX">

<div class="inputContainer" v-if="type==='view'">
  <div class="input">
      <input type="email" placeholder="Room Code" v-model="code" maxlength="4" autocomplete = "off" autocapitalize="none"> 
  </div>
</div>

</transition>

<br>

<transition enter-active-class="animated flipInX" leave-active-class="animated flipOutX">

<div class="inputContainer" v-if="sub && type==='join' || sub && type=='create'">
  <br>
  <div class="input">
      <input type="email" placeholder="Username" v-model="username" maxlength="10" autocapitalize="none">
  </div>
  </div>

</transition>

<br>

<transition enter-active-class="animated slideInRight" leave-active-class="animated slideOutLeft">
  <div class="inputContainer" v-if="sub && type=='view'">
      <button class="glow-on-hover" v-on:click="view">View Room</button>
    </div>
</transition>

<transition enter-active-class="animated slideInRight" leave-active-class="animated slideOutLeft">
  <div class="inputContainer" v-if="sub && type==='join' && name">
      <button class="glow-on-hover" v-on:click="join">Join Room</button>
    </div>
</transition>

<br>

<transition enter-active-class="animated slideInRight" leave-active-class="animated slideOutLeft">
  <div class="inputContainer" v-if="sub && type=='create' && name">
      <button class="glow-on-hover" v-on:click="create">Create Room</button>
    </div>
</transition>



<!--
<div class="inputContainer animated bounceInUp">
  <div class="input">
      <input type="email" placeholder="Room Code" v-model="code" maxlength="4" autocomplete = "off" autocapitalize="none">
      <input type="text" placeholder="Username" v-model="username" maxlength="10"> 
  </div>
  

</div>-->
<!--
<br>

<transition enter-active-class="animated flipInX" leave-active-class="animated flipOutX">
<div class="inputContainer">
  <div class="input">
      <input type="email" placeholder="Username" v-model="username" maxlength="10" autocapitalize="none">
  </div>
  </div>
</transition>

<br>

<transition enter-active-class="animated slideInLeft" leave-active-class="animated slideOutRight">
  <div class="inputContainer">
      <button class="glow-on-hover" v-on:click="join">Join Room</button>
    </div>
</transition>

<br>

<transition enter-active-class="animated slideInRight" leave-active-class="animated slideOutLeft">
  <div class="inputContainer">
      <button class="glow-on-hover" v-on:click="create">Create Room</button>
    </div>
</transition>

-->

</div>
</template>

<script>

import axios from 'axios'

export default {
  name: 'Landing',
  data() {
    return {
      code: '',
      username: '',
      selected: false,
      type: null
    }
  },
  methods: {
    initialRoom(event){
      if(event){
        this.selected = true
        this.type = "join"
      }
    },
    initialCreate(event){
      if(event){
        this.selected = true
        this.type = "create"
      }
    },
    initialView(event){
      if(event){
        this.selected = true
        this.type = "view"
      }
    },
    addCode() {
      this.code.push({code: this.code})
    },
    addName() {
      this.username.push({username: this.username})
    },
    view(event){
      let self = this;
      console.log("View")
      var room="/api/rooms/" + this.code
        axios.get(room).then(response => {
      // JSON responses are automatically parsed.
          console.log("Room found.")
          self.$router.push("/spectator/" + self.code)
        }).catch(function (error) {
          self.showRoomError({message: "Room " + self.code + " does not exist!"})
          return;
    })
  
    },
    join: function (event) {
      let self = this;
      if (event) {
        var room="/api/rooms/" + this.code
        axios.get(room).then(response => {
      // JSON responses are automatically parsed.
          console.log("Room found.")
          var userPost = "api/rooms/" + this.code + "/adduser"
          axios.post(userPost, { user_name: self.username}).then(response => {
            console.log("Player added.")
            self.$router.push("/lobby/" + self.code + "/" + self.username)
          }).catch(function (error) {
            self.showNameError({message: "Username " + self.username + " already exists!"})
            return;
          })
        }).catch(function (error) {
          self.showRoomError({message: "Room " + self.code + " does not exist!"})
          return;
    })

      }
    },
    create: function (event) {
      let self = this;
      if (event) {
        var room="/api/rooms/" + this.code
        axios.get(room).then(response => {
      // JSON responses are automatically parsed.
        self.showRoomCError({message: "Room " + self.code + " already exists!"})
        return;
    }).catch(function (error) {
      console.log("room ok to create")
      axios.post("/api/rooms/", 
      {
        user_list: [self.username],
        host: self.username,
        room_code: self.code,
        state: "W"
      }
      ).then(response => {
        console.log("room created, entering...")
        self.$router.push("/lobby/" + self.code + "/" + self.username)
      }).catch(function (error) {
        console.log(error)
        return;
      })
    })
      }
    },
    output: function(){
      console.log("10 seconds have succumbed to the time master, master of all time and space. None is beyond his grasp, the flowing sands of time lightly and tenderly shift through his all encompasing hands. You cannot escape him for he is immortal; As you get older, he gets younger. \n lo and behold, for epoch man himself looks directly in the face of the time master. For while the time master progresses steadily forever into that as what we know as the great and everpresent void of spacetime, epoch man journeys in the golden span of 1901 to 2038 in the year of our lord. Epoch man knows all that is and ever was for this era. He knows of your failures, embarrassments, secrets, and most prevalent; your future. while the time master must walk alongside you, epoch man is and has been where you are and are not. Who is more powerful? ...Only time will tell.")
      //this.showRoomCError({message: "10 seconds have succumbed to the time master, master of all time and space. None is beyond his grasp, the flowing sands of time lightly and tenderly shift through his all encompasing grasp."})
    }
  },

  computed: {
      sub: function() {
        //console.log(this.code.length)
        return this.code.length == 4
    },
      name: function(){
        //console.log(this.username.length)
        return this.username.length >= 1
      }
  },
  mounted: function () {
      window.setInterval(() => {
        this.output()
  }, 10000)
},
notifications: {
      showRoomError: { 
        title: 'Invalid Room',
        message: 'Room does not exist.',
        type: 'error' 
      },
      showRoomCError: { 
        title: 'Room Exists',
        message: 'Room already exists!',
        type: 'error' 
      },
      showNameError: { 
        title: 'Username Taken',
        message: 'That username is already taken!',
        type: 'error' 
      }
    }
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.7.2";

h1 {
  color: #6EB4EC;
  font-size: 100px;
  /*background: -webkit-linear-gradient(290deg, #6eb4ec, #6bb667); 
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;*/
  
}

.logoContainer {
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-user-select: none; /* Safari */        
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* IE10+/Edge */
    user-select: none; /* Standard */
}

* {
  box-sizing: border-box;
}

body {
  background-color: #333;
}

.inputContainer {
  display: flex;
  align-items: center;
  justify-content: center;
}

input[type=email], textarea {
  -webkit-transition: all 0.30s ease-in-out;
  -moz-transition: all 0.30s ease-in-out;
  -ms-transition: all 0.30s ease-in-out;
  -o-transition: all 0.30s ease-in-out;
  outline: none;
  padding: 3px 0px 3px 3px;
  margin: 5px 1px 3px 0px;
  border: 1px solid #6eb4ec;
  border-radius: 50px;
  width: 350px;
  height: 75px;
  background: transparent;
  text-align: center;
  color: transparent;
  text-shadow: 0 0 0 white;
  font-size: 30px;
}
 

input[type=email]:focus, textarea:focus {
  box-shadow: 0 0 5px rgba(81, 203, 238, 1);
  padding: 3px 0px 3px 3px;
  margin: 5px 1px 3px 0px;
  border: 1px solid rgba(81, 203, 238, 1);
  outline:none;
}

.glow-on-hover {
    width: 350px;
    height: 75px;
    border: 1px solid #6eb4ec;
    padding: 3px 0px 3px 3px;
    margin: 5px 1px 3px 0px;
    outline: none;
    color: #fff;
    background: #333;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 10px;
    font-size: 30px;
}

.glow-on-hover:before {
    content: '';
    background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
    position: absolute;
    top: -2px;
    left:-2px;
    background-size: 400%;
    z-index: -1;
    filter: blur(5px);
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    animation: glowing 20s linear infinite;
    opacity: 0;
    transition: opacity .3s ease-in-out;
    border-radius: 10px;
}

.glow-on-hover:active {
    color: #000
}

.glow-on-hover:active:after {
    background: transparent;
}

.glow-on-hover:hover:before {
    opacity: 1;
}

.glow-on-hover:after {
    z-index: -1;
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: #111;
    left: 0;
    top: 0;
    border-radius: 10px;
}

@keyframes glowing {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
}

.divider{
    width:5px;
    height:auto;
    display:inline-block;
}

</style>
