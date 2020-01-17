import Vue from 'vue'
import VueRouter from 'vue-router'
import PageNotFound from "./components/PageNotFound.vue"
import Landing from "./components/Landing.vue"
import lobby from "./components/lobby.vue"
import game from "./components/game.vue"
import voting from "./components/voting.vue"
import results from "./components/results.vue"
import spectator from "./components/spectator.vue"

Vue.use(VueRouter)

export default new VueRouter({
  mode: "history",
    routes: [
        {
            path: '/',
            name: '1DIOT',
            component: Landing,
            meta: {
                title: '1DIOT',
                metaTags: [
                  {
                    name: 'description',
                    content: 'One Idiot - find the odd one out!'
                  },
                  {
                    property: 'og:description',
                    content: 'One Idiot - find the odd one out!'
                  }
                ]
              }

        },
        {
          path: '/lobby/:code/:username',
          name: 'Lobby',
          component: lobby,
          meta: {
              title: '1DIOT',
              metaTags: [
                {
                  name: 'description',
                  content: 'One Idiot - find the odd one out!'
                },
                {
                  property: 'og:description',
                  content: 'One Idiot - find the odd one out!'
                }
              ]
            }

      },
      {
        path: '/game/:code/:username',
        name: ':code',
        component: game,
        meta: {
            title: '1DIOT',
            metaTags: [
              {
                name: 'description',
                content: 'One Idiot - find the odd one out!'
              },
              {
                property: 'og:description',
                content: 'One Idiot - find the odd one out!'
              }
            ]
          }

    },
    {
      path: '/spectator/:code',
      name: 'Specator',
      component: spectator,
      meta: {
          title: '1DIOT',
          metaTags: [
            {
              name: 'description',
              content: 'One Idiot - find the odd one out!'
            },
            {
              property: 'og:description',
              content: 'One Idiot - find the odd one out!'
            }
          ]
        }

       },
    {
      path: '/voting/:code/:username',
      name: 'Voting',
      component: voting,
      meta: {
          title: '1DIOT',
          metaTags: [
            {
              name: 'description',
              content: 'One Idiot - find the odd one out!'
            },
            {
              property: 'og:description',
              content: 'One Idiot - find the odd one out!'
            }
          ]
        }

       },
       {
        path: '/results/:code/:username',
        name: 'Results',
        component: results,
        meta: {
            title: '1DIOT',
            metaTags: [
              {
                name: 'description',
                content: 'One Idiot - find the odd one out!'
              },
              {
                property: 'og:description',
                content: 'One Idiot - find the odd one out!'
              }
            ]
          }
  
         },
        { 
        path: "*", 
        component: PageNotFound,
        meta: {
            title: 'Not Found',
            metaTags: [
              {
                name: 'description',
                content: 'Page not found'
              },
              {
                property: 'og:description',
                content: 'Page not found'
              }
            ]
          }

        }
    ]
})
