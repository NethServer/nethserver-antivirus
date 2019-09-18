<template>
  <div>
    <h1>{{$t('dashboard.title')}}</h1>
      <!-- error message -->
      <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
        <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
          <span class="pficon pficon-close"></span>
        </button>
        <span class="pficon pficon-error-circle-o"></span>
        {{ errorMessage }}.
      </div>

      <div v-show="!uiLoaded" class="spinner spinner-lg"></div>
      <div v-show="uiLoaded">
        
      </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  props: {
  },
  mounted() {
    ////
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null
    };
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage
    },
    closeErrorMessage() {
      this.errorMessage = null
    }
  }
};
</script>

<style>
</style>
