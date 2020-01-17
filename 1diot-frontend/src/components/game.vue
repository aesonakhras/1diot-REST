<template>
<div>
    <div v-if="sub < 1">
    <div class="centered">
     <div class="time">{{ time }}</div>
     </div>
    <div class="centered">
        <button class="glow-on-hover" v-on:click="show = !show">Show role</button>
    </div>
        <h1  style="font-size: 1.3rem" v-if="faker === $route.params.username && show">(You are the odd one out)</h1>
        <h1  style="font-size: 1.3rem" v-if="faker != $route.params.username && show">(You are not the odd one out)</h1>

   
    <h1>Question:</h1>
    <div class="centered">

        <div v-if="$route.params.username != faker">
            {{gQuestion}}
        </div>

        <div v-if="$route.params.username === faker">
            {{bQuestion}}
        </div>

    </div>
    <br>

    <div class="centered">
            <input type="text" placeholder="Answer" v-model="ans" :disabled="sub == 1">
    </div>
    <div class="centered">
        <button class="glow-on-hover" v-on:click="submit" :disabled="sub == 1">submit</button>
    </div>

    <br>
    <hr>
    <br>
    <div class="centered">
        <button class="glow-on-hover" v-on:click="left">Leave game (ends game)</button>
    </div>
    </div>
    <div v-else>
        <div class="centered">You have submitted your answer!</div>
    </div>

</div>
</template>

<script>

import axios from 'axios'

    export default {
        name: 'game',
        data() {
            return {
            players: [],
            state: "A",
            playerReady: "A",
            host: "",
            faker: "",
            qID: 1,
            sub: 0,
            ans: "",
            gQuestion: "",
            bQuestion: "",
            stateTimer: null,
            gameTimer: null,
            time: 60,
            show: false

        }},
        methods: {
            submit: function (event) {
                let self = this

                if(event){
                    if(this.sub === 0){
                        axios.post("/api/rooms/" + self.$route.params.code + "/submitanswer", {user_name: self.$route.params.username, answer: self.ans})
                        this.sub = 1
                    }
                    else{
                        self.showAnsErr({message: "You've already submitted an answer!"})
                    }
                }
                
            },
            autoSubmit(){
                let self = this
                if(this.sub === 0){
                        axios.post("/api/rooms/" + self.$route.params.code + "/submitanswer", {user_name: self.$route.params.username, answer: self.ans})
                        this.sub = 1
                    }
            },
            leaveGame(){
                let self = this
                axios.post("/api/rooms/" + self.$route.params.code + "/setstate", { state: "D"}).then(function (result) {
                    //self.playerReady = "N"
                    window.clearInterval(self.stateTimer)
                    window.clearInterval(self.gameTimer)
                    axios.post("/api/rooms/" + self.$route.params.code + "/removeuser", {user_name: self.$route.params.username}).then(function (){self.$router.push("/").catch(err => {
                        //do nothing
                    })}).catch(function (error) {
                        self.showGetErr({message: error, title: "leaveGame Error"})
                        return;
                    })
                }).catch(function (error) {
                    self.showGetErr({message: error, title: "leaveGame Error"})
                    return;
                })
            },
            gotoVoting(){
                window.clearInterval(this.stateTimer)
                window.clearInterval(this.gameTimer)
                //self.playerReady = "N"
                this.$router.push("/voting/" + this.$route.params.code + "/" + this.$route.params.username).catch(err => {
                    //do nothing
                })
            },
            left: function (event) {
                if(event){
                    console.log("player left")
                    this.leaveGame()
                }
            },
            getState() {
                let self = this
                console.log("got state")
                axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
                    self.state = response.data.state

                    if(self.state === "V"){
                        self.gotoVoting()
                    }
                    else if(self.state === "D"){
                        self.leaveGame()
                    }
                }).catch(function (error) {
                        self.showGetErr({message: error, title: "getState error"})
                        return;
                })

                axios.get("/api/rooms/" + self.$route.params.code).then(function(result){
                    self.faker = result.data.user_wrong
                    console.log(self.faker)
                })

            },
            getInfo(){
                let self = this

                axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
                    self.host = response.data.host
                    self.faker = response.data.user_wrong
                    self.players = response.data.player_list
                    self.state = response.data.state
                    self.qID = response.data.question_id
                    axios.get("/api/questions/" + self.qID + "/wrong").then(function (response){
                        self.bQuestion = response.data.prompt
                    }).catch(function (error) {
                            self.showGetErr({message: error, title: "getInfo"})
                            self.getInfo()
                            return;
                    })
                    axios.get("/api/questions/" + self.qID + "/right").then(function (response){
                        self.gQuestion = response.data.prompt
                    }).catch(function (error) {
                            self.showGetErr({message: error, title: "getInfo"})
                            self.getInfo()
                            return;
                    })
                    }).catch(function (error) {
                        self.showGetErr({message: error, title: "getInfo"})
                        self.getInfo()
                        return;
                })
            }

        },
        asyncComputed: {
            getQ() {
                let self = this
                return(axios.get("/api/rooms/" + self.$route.params.code).then(response => response.data.host))
            }
        },
        created () {
            let self = this

            document.title = this.$route.params.code + " - Game"

            axios.get("/api/rooms/" + self.$route.params.code).then( function (response) {
                self.host = response.data.host
                self.faker = response.data.user_wrong
                self.players = response.data.player_list
                self.state = response.data.state
                self.qID = response.data.question_id
                axios.get("/api/questions/" + self.qID + "/wrong").then(function (response){
                    self.bQuestion = response.data.prompt
                }).catch(function (error) {
                        self.showGetErr({message: error, title: "created"})
                        self.getInfo()
                        return;
                })
                axios.get("/api/questions/" + self.qID + "/right").then(function (response){
                    self.gQuestion = response.data.prompt
                }).catch(function (error) {
                        self.showGetErr({message: error, title: "created"})
                        self.getInfo()
                        return;
                })
            }).catch(function (error) {
                        self.showGetErr({message: error, title: "created"})
                        self.getInfo()
                        return;
            })
        },
        mounted: function() {

            this.stateTimer = window.setInterval(() => {
                this.getState()
            }, 2000)

            this.gameTimer = window.setInterval(() => {
                if(this.time === 0){
                    this.autoSubmit()
                }
                else{
                    this.time = this.time - 1
                }
            }, 1000)
        },
        notifications: {
            showGetErr: { 
                title: 'Request Error',
                message: 'Issue goes here',
                type: 'error' 
            },
            showAnsErr: {
                title: "Already submitted!",
                message: 'issue',
                type: "error"
            },
            showOddNotif: {
                title: "You're the odd one out!",
                message: "Fool the other players!",
                type: "info"
            }
    }
    }
</script>

<style scoped>

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

.time {
    color: white;
    font-size: 1.5rem; 
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

input, select, {
    color: white;
}

input[type=text], select {
outline: none;
  width: 300px;
  height: 50px;
  color: white;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #6EB4EC;
  border-radius: 30px;
  background-color: rgb(20,20,20);
  box-sizing: border-box;
  font-size: 1rem;
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: rgb(214,214,214);
  font-size: 1rem;
  opacity: 1; /* Firefox */
}

:-ms-input-placeholder { /* Internet Explorer 10-11 */
  font-size: 1rem;
  color: rgb(214,214,214);
}

::-ms-input-placeholder { /* Microsoft Edge */
  font-size: 1rem;
  color: rgb(214,214,214);
}

.stack {
    display: flex;
    flex-direction: column;
}

</style>