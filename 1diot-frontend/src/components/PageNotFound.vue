
<template>
    <div class="info"></div>
</template>

<script>
export default {
    name: "Page not found",
     created: function() {
        // Redirect outside the app using plain old javascript
        window.location.href = "/404.html";
    }
}
</script>

<style>

.info {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: verdana;
  font-size: 2rem;
  color: #f5f5f5;
}

</style>