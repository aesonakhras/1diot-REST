<template>
<body>
  <head>
  <link rel="shortcut icon" type="image/png" href="/static/logo.ico"/>
  </head>
  <div id="app">
    <router-view></router-view>
    
  </div>
</body>
</template>

<script>


export default {
  name: 'app',
  watch: {
        $route(to, from) {
            document.title = to.meta.title || '1DIOT';
        }
},
computed: {
    pageTitle: function() {
        return this.$route.meta.title;
    }
},
created () {
    document.title = this.$route.meta.title;
}
}
</script>

<style>

body {
  background: rgb(20,20,20);
}

</style>
