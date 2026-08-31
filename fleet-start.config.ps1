# Per-repo fleet start config for repomix-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'repomix-mcp'
    BackendPort  = 10914
    FrontendPort = 10913
    HealthPath   = '/health'
    WebRoot      = 'D:\Dev\repos\repomix-mcp\web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'repomix_mcp.server:app'
        Env           = @{ WEB_PORT = '10914' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
