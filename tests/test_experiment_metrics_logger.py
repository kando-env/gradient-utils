import mock

from gradient_utils import MetricsLogger
from gradient_utils.metrics import get_metric_pushgateway, CollectorRegistry


@mock.patch("gradient_utils.metrics.get_metric_pushgateway", return_value="some_gateway")
@mock.patch("gradient_utils.metrics.get_job_id", return_value="some_id")
def test_should_create_metrics_logger_instance_with_required_parameters(
        get_job_id_patched, get_metric_pushgateway_patched):
    metrics_logger = MetricsLogger()

    assert metrics_logger.id == "some_id"
    assert metrics_logger.grouping_key is None
    assert metrics_logger.push_gateway == "some_gateway"
    assert isinstance(metrics_logger.registry, CollectorRegistry)


@mock.patch("gradient_utils.metrics.get_metric_pushgateway")
@mock.patch("gradient_utils.metrics.get_job_id")
def test_should_create_metrics_logger_instance_with_all_parameters(
        get_job_id_patched, get_metric_pushgateway_patched):
    grouping_key = {"key": "value"}
    registry = CollectorRegistry()
    push_gateway = "some.url"

    metrics_logger = MetricsLogger(
        "some_id",
        registry=registry,
        grouping_key=grouping_key,
        push_gateway=push_gateway,
    )

    assert metrics_logger.id == "some_id"
    assert metrics_logger.grouping_key == grouping_key
    assert metrics_logger.push_gateway == push_gateway
    assert metrics_logger.registry is registry
    get_job_id_patched.assert_not_called()
    get_metric_pushgateway_patched.assert_not_called()


@mock.patch("gradient_utils.metrics.Gauge")
def test_should_add_gauge_to_logger_instance(gauge_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_gauge"

    metrics_logger.add_gauge(metric_name)

    assert metric_name in metrics_logger._metrics
    assert metrics_logger._metrics[metric_name] == gauge_patched.return_value


@mock.patch("gradient_utils.metrics.Gauge")
def test_should_update_gauge_value(gauge_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_gauge"

    metrics_logger.add_gauge(metric_name)
    metrics_logger[metric_name].set(2)

    gauge_patched().set.assert_called_once_with(2),


@mock.patch("gradient_utils.metrics.Counter")
def test_should_add_counter_to_logger_instance(counter_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_counter"

    metrics_logger.add_counter(metric_name)

    assert metric_name in metrics_logger._metrics
    assert metrics_logger._metrics[metric_name] == counter_patched.return_value


@mock.patch("gradient_utils.metrics.Counter")
def test_should_update_counter_value(counter_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_counter"

    metrics_logger.add_counter(metric_name)
    metrics_logger[metric_name].inc(2)

    counter_patched().inc.assert_called_once_with(2),


@mock.patch("gradient_utils.metrics.Summary")
def test_should_add_summary_to_logger_instance(summary_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_summary"

    metrics_logger.add_summary(metric_name)

    assert metric_name in metrics_logger._metrics
    assert metrics_logger._metrics[metric_name] == summary_patched.return_value


@mock.patch("gradient_utils.metrics.Summary")
def test_should_update_summary_value(summary_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_summary"

    metrics_logger.add_summary(metric_name)
    metrics_logger[metric_name].observe(2)

    summary_patched().observe.assert_called_once_with(2),


@mock.patch("gradient_utils.metrics.Histogram")
def test_should_add_histogram_to_logger_instance(histogram_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_histogram"

    metrics_logger.add_histogram(metric_name)

    assert metric_name in metrics_logger._metrics
    assert metrics_logger._metrics[metric_name] == histogram_patched.return_value


@mock.patch("gradient_utils.metrics.Histogram")
def test_should_update_histogram_value(histogram_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_histogram"

    metrics_logger.add_histogram(metric_name)
    metrics_logger[metric_name].observe(2)

    histogram_patched().observe.assert_called_once_with(2),


@mock.patch("gradient_utils.metrics.Info")
def test_should_add_info_to_logger_instance(info_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_info"

    metrics_logger.add_info(metric_name)

    assert metric_name in metrics_logger._metrics
    assert metrics_logger._metrics[metric_name] == info_patched.return_value


@mock.patch("gradient_utils.metrics.Info")
def test_should_update_info_value(info_patched):
    metrics_logger = MetricsLogger("some_id")
    metric_name = "some_info"

    metrics_logger.add_info(metric_name)
    metrics_logger[metric_name].info(2)

    info_patched().info.assert_called_once_with(2),


@mock.patch("gradient_utils.metrics.push_to_gateway")
def test_should_use_push_to_gateway_to_log_metrics(push_to_gateway_patched):
    grouping_key = {"key": "value"}
    registry = CollectorRegistry()
    metrics_logger = MetricsLogger(
        "some_id",
        registry=registry,
        grouping_key=grouping_key,
    )

    metrics_logger.push_metrics()

    push_to_gateway_patched.assert_called_once_with(
        gateway=get_metric_pushgateway(),
        job="some_id",
        registry=registry,
        grouping_key=grouping_key,
        timeout=30,
    )
