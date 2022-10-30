<script setup>

</script>




<template>
  <div class = "search_box ">
    <p class = "mb-0">Starting</p>
    <input
      :value="starting"
      @input="event => starting = event.target.value">
      <p class = "mt-5 mb-0">Destination</p>
    <input
      :value="destination"
      @input="event => destination = event.target.value">
      <div>
        <button class="mt-5">Search</button>
      </div>

  </div>

 
</template>







<style>
.p{
  margin-top: 0px;
}
</style>
