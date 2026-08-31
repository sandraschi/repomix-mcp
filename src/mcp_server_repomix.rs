use schemars::JsonSchema;
use serde::Deserialize;
use std::env;
use zed::settings::ContextServerSettings;
use zed_extension_api::{
    self as zed, serde_json, Command, ContextServerConfiguration, ContextServerId, Project, Result,
};

const PACKAGE_NAME: &str = "repomix";
const PACKAGE_VERSION: &str = "latest";
const SERVER_COMMAND: &str = "repomix";

#[derive(Debug, Deserialize, JsonSchema)]
struct RepomixContextExtensionSettings {
    #[serde(default)]
    repomix_path: Option<String>,
}

struct RepomixContextExtension;

impl zed::Extension for RepomixContextExtension {
    fn new() -> Self {
        Self
    }

    fn context_server_command(
        &mut self,
        _context_server_id: &ContextServerId,
        project: &Project,
    ) -> Result<Command> {
        let version = zed::npm_package_installed_version(PACKAGE_NAME)?;
        if version.as_deref() != Some(PACKAGE_VERSION) {
            zed::npm_install_package(PACKAGE_NAME, PACKAGE_VERSION)?;
        }

        let settings = ContextServerSettings::for_project("mcp-server-repomix", project)?;

        let settings_struct: RepomixContextExtensionSettings = match settings.settings {
            Some(v) => serde_json::from_value(v).map_err(|e| e.to_string())?,
            None => RepomixContextExtensionSettings {
                repomix_path: None,
            },
        };

        let mut args = Vec::new();
        args.push("--mcp".to_string());

        let command_path = if let Some(custom_path) = settings_struct.repomix_path {
            custom_path
        } else {
            env::current_dir()
                .unwrap()
                .join("node_modules")
                .join(".bin")
                .join(SERVER_COMMAND)
                .to_string_lossy()
                .to_string()
        };

        Ok(Command {
            command: command_path,
            args,
            env: Default::default(),
        })
    }

    fn context_server_configuration(
        &mut self,
        _context_server_id: &ContextServerId,
        project: &Project,
    ) -> Result<Option<ContextServerConfiguration>> {
        let installation_instructions =
            include_str!("../configuration/installation_instructions.md").to_string();

        let settings = ContextServerSettings::for_project("mcp-server-repomix", project);

        let mut default_settings =
            include_str!("../configuration/default_settings.jsonc").to_string();

        if let Ok(user_settings) = settings {
            if let Some(settings_value) = user_settings.settings {
                if let Ok(repomix_settings) =
                    serde_json::from_value::<RepomixContextExtensionSettings>(settings_value)
                {
                    if let Some(repomix_path) = repomix_settings.repomix_path {
                        default_settings = default_settings.replace(
                            "\"\"",
                            &format!("\"{}\"", repomix_path),
                        );
                    }
                }
            }
        }

        let settings_schema = serde_json::to_string(&schemars::schema_for!(
            RepomixContextExtensionSettings
        ))
        .map_err(|e| e.to_string())?;

        Ok(Some(ContextServerConfiguration {
            installation_instructions,
            default_settings,
            settings_schema,
        }))
    }
}

zed::register_extension!(RepomixContextExtension);
