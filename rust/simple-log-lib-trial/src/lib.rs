mod trial;

use std::fs::OpenOptions;

// Ref: https://stackoverflow.com/a/43093371/6323360
use std::sync::Once;
static INIT: Once = Once::new();

pub use crate::trial::Trial;
pub use log::{debug, error, info, log, trace, warn, Level};

use simplelog::{
    CombinedLogger, ConfigBuilder, LevelFilter, TermLogger, TerminalMode, WriteLogger,
};

pub fn setup_logger() {
    INIT.call_once(|| {
        let mut config_builder = ConfigBuilder::new();
        config_builder.set_time_format_str("%Y-%m-%d_%H:%M:%S");
        let is_local_time = true;
        config_builder.set_time_to_local(is_local_time);
        let config = config_builder.build();

        CombinedLogger::init(vec![
            TermLogger::new(LevelFilter::Debug, config.clone(), TerminalMode::Mixed),
            WriteLogger::new(
                LevelFilter::Debug,
                config.clone(),
                OpenOptions::new()
                    .append(true)
                    .create(true)
                    .open("output/debug.log")
                    .unwrap(),
            ),
        ])
        .unwrap();
    });
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_log_creation() {
        // Arrange
        setup_logger();

        // Act
        debug!("Debug");
        error!("Error!");
        info!("Info!");
        log!(Level::Info, "Log");
        trace!("Trace");
        warn!("Warn");
    }

    #[test]
    fn test_add_two_numbers_correctly() {
        // Arrange
        setup_logger();
        let trial = Trial::new();
        let num1 = 5;
        let num2 = 6;

        // Act
        let sum1 = trial.add(num1, num2);

        // Assert
        assert_eq!(5 + 6, sum1);
    }
}
