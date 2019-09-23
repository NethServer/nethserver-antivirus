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

      <!-- empty state: rspamd and squidclamav not installed -->
      <div class="row blank-slate-pf" v-if="uiLoaded && !dashboardData.rspamd.installed && !dashboardData.squidclamav.installed">
        <div class="blank-slate-pf-icon">
          <div class="fa fa-exclamation-circle"></div>
            <h1>{{$t('dashboard.no_instance_installed')}}</h1>
          </div>
        </div>
      </div>

      <!-- rspamd -->
      <div class="row" v-if="uiLoaded && dashboardData.rspamd.installed">
        <h4 class="right gray mg-top-20">
          {{$t('dashboard.since')}}
          <b>{{ rspamdSince | dateFormat }}</b>
        </h4>
        <h3>{{ $t('dashboard.email_protection') }}</h3>
        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            <span
              :class="dashboardData.rspamd.active ? 'fa fa-check green' : 'fa fa-times red'"
            ></span>
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.status') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ dashboardData.rspamd.malwareFound }}
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.malware_found') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ dashboardData.rspamd.signatures }}
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.signatures_loaded') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ (dashboardData.rspamd.memoryUsedKb * 1024) | byteFormat }}
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.memory_used') }}
            </span>
          </span>
        </div>
      </div>

      <!-- rspamd malware chart -->
      <div class="row">
        <div
          id="pie-chart-rspamd"
          class="pie-chart"
          v-show="uiLoaded && dashboardData.rspamd.installed && dashboardData.rspamd.malwareStats.length > 0"
        ></div>
        <div v-show="uiLoaded && dashboardData.rspamd.installed && dashboardData.rspamd.malwareStats.length == 0" class="empty-piechart">
          <div class="fa fa-pie-chart"></div>
          <div>{{$t('dashboard.no_data_available')}}</div>
        </div>
      </div>

      <div class="divider" v-if="uiLoaded && dashboardData.rspamd.installed && dashboardData.squidclamav.installed"></div>

      <!-- squidclamav -->
      <div class="row" v-if="uiLoaded && dashboardData.squidclamav.installed">
        <h4 class="right gray mg-top-20">
          {{$t('dashboard.since')}}
          <b>{{ squidclamavSince | dateFormat }}</b>
        </h4>
        <h3>{{ $t('dashboard.web_protection') }}</h3>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            <span
              :class="dashboardData.squidclamav.active ? 'fa fa-check green' : 'fa fa-times red'"
            ></span>
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.status') }}
            </span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span
            class="card-pf-utilization-card-details-count stats-count"
          >{{ dashboardData.squidclamav.malwareFound }}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.malware_found') }}</span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ dashboardData.squidclamav.signatures }}</span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span
              class="card-pf-utilization-card-details-line-2 stats-text"
            >{{ $t('dashboard.signatures_loaded') }}</span>
          </span>
        </div>

        <div class="stats-container col-xs-12 col-sm-3 col-md-3 col-lg-3">
          <span class="card-pf-utilization-card-details-count stats-count">
            {{ (dashboardData.squidclamav.memoryUsedKb * 1024) | byteFormat }}
          </span>
          <span class="card-pf-utilization-card-details-description stats-description">
            <span class="card-pf-utilization-card-details-line-2 stats-text">
              {{ $t('dashboard.memory_used') }}
            </span>
          </span>
        </div>
      </div>
      
      <!-- squidclamav malware chart -->
      <div class="row">
        <div
          id="pie-chart-squidclamav"
          class="pie-chart"
          v-show="uiLoaded && dashboardData.squidclamav.installed && dashboardData.squidclamav.malwareStats.length > 0"
        ></div>
        <div v-show="uiLoaded && dashboardData.squidclamav.installed && dashboardData.squidclamav.malwareStats.length == 0" class="empty-piechart">
          <div class="fa fa-pie-chart"></div>
          <div>{{$t('dashboard.no_data_available')}}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  props: {
  },
  mounted() {
    this.getDashboardData()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      dashboardData: {
        "rspamd": null,
        "squidclamav": null
      },
      rspamdSince: 0,
      squidclamavSince: 0
    };
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage
    },
    closeErrorMessage() {
      this.errorMessage = null
    },
    getDashboardData() {
      var ctx = this;
      nethserver.exec(
        ["nethserver-antivirus/dashboard/read"],
        null,
        null,
        function(success) {
          success = JSON.parse(success);
          ctx.dashboardData = success;
          ctx.convertSinceTime();
          ctx.uiLoaded = true;

          setTimeout(function() {
            if (ctx.dashboardData.rspamd.installed) {
              ctx.initMalwareChart('rspamd');
            }
            if (ctx.dashboardData.squidclamav.installed) {
              ctx.initMalwareChart('squidclamav');
            }
          }, 250);
        },
        function(error) {
          ctx.showErrorMessage(ctx.$i18n.t("dashboard.error_getting_dashboard_data"), error)
        }
      );
    },
    convertSinceTime() {
      if (this.dashboardData.rspamd.sinceIso) {
        this.rspamdSince = new Date(this.dashboardData.rspamd.sinceIso).getTime();
      } else {
        this.rspamdSince = 0
      }

      if (this.dashboardData.squidclamav.sinceIso) {
        this.squidclamavSince = new Date(this.dashboardData.squidclamav.sinceIso).getTime();
      } else {
        this.squidclamavSince = 0
      }
    },
    initMalwareChart(instance) {
      var c3ChartDefaults = $().c3ChartDefaults();

      var pieData = {
        type : 'pie',
        columns: this.groupSmallPieCategories(this.dashboardData[instance].malwareStats)
      };

      var pieChartConfig = c3ChartDefaults.getDefaultPieConfig();
      pieChartConfig.bindto = '#pie-chart-' + instance;
      pieChartConfig.data = pieData;
      pieChartConfig.legend = {
        show: true,
        position: 'right'
      };
      pieChartConfig.size = {
        width: 450,
        height: 220
      };
      pieChartConfig.color={ pattern:[
        $.pfPaletteColors.orange,
        $.pfPaletteColors.red,
        $.pfPaletteColors.blue,
        $.pfPaletteColors.green,
        $.pfPaletteColors.gold,
        $.pfPaletteColors.purple,
        $.pfPaletteColors.black
      ]};
      var pieChartLegend = c3.generate(pieChartConfig);
    },
    groupSmallPieCategories(pieData) {
      var threshold = 5
      var groupedLabel = this.$i18n.t("dashboard.other")
      var groupedValue = 0
      var i = pieData.length

      while (i--) {
        if (pieData[i][1] < threshold) {
            groupedValue += pieData[i][1]
            pieData.splice(i, 1);
        }
      }

      if (groupedValue > 0) {
        // some categories have been grouped together
        pieData.push([ groupedLabel, groupedValue])
      }
      return pieData
    }
  }
};
</script>

<style>
.row {
  padding-left: 20px;
  padding-right: 20px;
}

.empty-piechart {
  margin-top: 2em;
  margin-bottom: 2em;
  text-align: center;
  color: #9c9c9c;
}
.empty-piechart .fa {
  font-size: 200px;
  color: #bbbbbb;
}
</style>
