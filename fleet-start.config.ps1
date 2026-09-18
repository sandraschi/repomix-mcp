# Per-repo fleet start config for repomix-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'repomix-mcp'
    BackendPort  = 11207
    FrontendPort = 11206
    HealthPath   = '/health'
    WebRoot      = 'web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'repomix_mcp.server:app'
        SyncExtras    = @('dev')
        Env           = @{ WEB_PORT = '11207' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
