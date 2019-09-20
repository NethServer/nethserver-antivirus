<template>
  <div>
    <h1>{{$t('settings.title')}}</h1>
    
    <!-- error message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
      <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
        <span class="pficon pficon-close"></span>
      </button>
      <span class="pficon pficon-error-circle-o"></span>
      {{ errorMessage }}.
    </div>

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
    <div v-if="uiLoaded">
      <form class="form-horizontal mg-top-30" v-on:submit.prevent="saveConfiguration">
        <!-- official signatures -->
        <div class="form-group">
          <label
            class="col-sm-2 control-label"
          >{{$t('settings.official_signatures')}}</label>
          <div class="col-sm-5">
            <input
              @click="toggleOfficialSignatures()"
              v-model="officialSignatures"
              type="checkbox"
              class="form-control"
            >
          </div>
        </div>
        <!-- unofficial signatures rating -->
        <div class="form-group">
          <label
            class="col-sm-2 control-label"
          >{{$t('settings.unofficial_signatures_rating')}}</label>
          <div class="col-sm-2">
            <select
              type="text"
              class="combobox form-control"
              v-model="clamdConfig.UnofficialSignaturesRating"
            >
              <option
                v-for="(rating, index) in unofficialSignaturesRatingList"
                v-bind:key="index"
                :value="rating"
              >
                {{ rating | capitalize }}
              </option>
            </select>
          </div>
        </div>
        <!-- save button -->
        <div class="form-group">
          <label class="col-sm-2 control-label">
          </label>
          <div class="col-sm-5">
            <button 
              class="btn btn-primary" 
              type="submit"
            >
              {{$t('save')}}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Settings",
  mounted() {
    this.getConfig()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      clamdConfig: null,
      unofficialSignaturesRatingList: [
        "low",
        "medium",
        "high"
      ]
    }
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error)
      this.errorMessage = errorMessage;
    },
    closeErrorMessage() {
      this.errorMessage = null;
    },
    getConfig() {
      var ctx = this;
      nethserver.exec(
        ["nethserver-antivirus/settings/read"],
        null,
        null,
        function(success) {
          success = JSON.parse(success);
          ctx.clamdConfig = success.configuration.props;
          ctx.officialSignatures = ctx.clamdConfig.OfficialSignatures === "enabled";
          ctx.uiLoaded = true;
        },
        function(error) {
          ctx.showErrorMessage(ctx.$i18n.t("settings.error_reading_configuration"), error)
        }
      );
    },
    saveConfiguration() {
      this.errorMessage = null;

      var configValidate = {
        "OfficialSignatures": this.clamdConfig.OfficialSignatures,
        "UnofficialSignaturesRating": this.clamdConfig.UnofficialSignaturesRating
      }
      var ctx = this;
      nethserver.exec(
        ["nethserver-antivirus/settings/validate"],
        configValidate,
        null,
        function(success) {
          ctx.configurationValidationSuccess(configValidate)
        },
        function(error, data) {
          // no need for field highlighting
          ctx.showErrorMessage(ctx.$i18n.t("settings.error_validating_configuration"), error)
          ctx.uiLoaded = true
        }
      );
    },
    configurationValidationSuccess(configValidate) {
      this.uiLoaded = false
      nethserver.notifications.success = this.$i18n.t("settings.configuration_update_successful");
      nethserver.notifications.error = this.$i18n.t("settings.configuration_update_failed");

      var ctx = this
      nethserver.exec(
        ["nethserver-antivirus/settings/update"],
        configValidate,
        function(stream) {
          console.info("antivirus-configuration-update", stream); /* eslint-disable-line no-console */
        },
        function(success) {
          ctx.getConfig()
        },
        function(error) {
          console.error(error)  /* eslint-disable-line no-console */
          ctx.uiLoaded = true
        }
      );
    },
    toggleOfficialSignatures() {
      if (this.clamdConfig.OfficialSignatures === "enabled") {
        this.clamdConfig.OfficialSignatures = "disabled"
      } else {
        this.clamdConfig.OfficialSignatures = "enabled"
      }
    }
  }
};
</script>

<style scoped>
.mg-top-30 {
  margin-top: 30px;
}
</style>
