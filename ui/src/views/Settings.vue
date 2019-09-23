<template>
  <div>
    <h1>{{$t('settings.title')}}</h1>

    <!-- info -->
    <div class="alert alert-info">
      <span class="pficon pficon-info"></span>
      {{$t('settings.info_notification')}}
    </div>

    <!-- memory warning -->
    <div
      class="alert alert-warning"
      v-if="uiLoaded && (totalMemory < 4000) && officialSignatures"
    >
      <span class="pficon pficon-warning-triangle-o"></span>
      {{$t('settings.memory_warning')}}
    </div>
    
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
      <form class="form-horizontal" v-on:submit.prevent="saveConfiguration">
        <!-- official signatures -->
        <div class="form-group">
          <label class="col-sm-3 control-label">
            {{$t('settings.official_signatures')}}
            <doc-info
              :placement="'top'"
              :title="$t('settings.official_signatures')"
              :chapter="'official_signatures'"
              :inline="true"
            ></doc-info>
          </label>
          <div class="col-sm-4">
            <input
              v-model="officialSignatures"
              type="checkbox"
              class="form-control"
            >
          </div>
        </div>
        <!-- unofficial signatures rating -->
        <div class="form-group">
          <label class="col-sm-3 control-label">
            {{$t('settings.unofficial_signatures_rating')}}
            <doc-info
              :placement="'top'"
              :title="$t('settings.unofficial_signatures_rating')"
              :chapter="'unofficial_signatures_ratings'"
              :inline="true"
            ></doc-info>
          </label>
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
          <label class="col-sm-3 control-label">
          </label>
          <div class="col-sm-4">
            <button 
              :disabled="saving"
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
      officialSignatures: false,
      unofficialSignaturesRatingList: [
        "low",
        "medium",
        "high"
      ],
      totalMemory: 0,
      saving: false,
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
        {
          "appInfo": "clamdConfig"
        },
        null,
        function(success) {
          success = JSON.parse(success);
          ctx.clamdConfig = success.configuration.props;
          ctx.getConfigSuccess();
        },
        function(error) {
          ctx.showErrorMessage(ctx.$i18n.t("settings.error_reading_configuration"), error)
        }
      );
    },
    getConfigSuccess() {
      this.officialSignatures = this.clamdConfig.OfficialSignatures === "enabled";
      var ctx = this;
      nethserver.exec(
        ["nethserver-antivirus/settings/read"],
        {
          "appInfo": "totalMemory"
        },
        null,
        function(success) {
          success = JSON.parse(success);
          ctx.totalMemory = success.totalMemory;
          ctx.uiLoaded = true;
        },
        function(error) {
          ctx.showErrorMessage(ctx.$i18n.t("settings.error_reading_total_memory"), error)
        }
      );
    },
    saveConfiguration() {
      this.saving = true
      this.errorMessage = null

      var configValidate = {
        "OfficialSignatures": this.officialSignatures ? "enabled" : "disabled",
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
          this.saving = false
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
          ctx.saving = false
          ctx.getConfig()
        },
        function(error) {
          console.error(error)  /* eslint-disable-line no-console */
          ctx.saving = false
          ctx.uiLoaded = true
        }
      );
    }
  }
};
</script>

<style scoped>
</style>
