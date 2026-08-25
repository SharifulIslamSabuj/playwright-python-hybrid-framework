// Jenkinsfile — implements the same docs/10-Automation-Strategy.md §18/§19/§21/§22
// and docs/11-Framework-Architecture.md §27/§29/§30/§31 design that
// .github/workflows/ci.yml already implements, on a second CI/CD platform,
// per the QA-Lead-approved Step 19 three-platform scope
// (docs/19-CI-CD.md).
//
// This pipeline runs the SAME Python + Playwright + Pytest framework and
// the SAME 22 currently implemented, approved automated Test Cases as
// GitHub Actions — no test logic is duplicated or forked for Jenkins; this
// file only orchestrates the existing `tests/` suite via pytest markers
// already registered in pyproject.toml.
//
// ASSUMPTIONS (this Jenkinsfile does not assume Jenkins is installed,
// configured, or connected to this repository — docs/19-CI-CD.md records
// its status as "Implemented locally / Externally executed: NO"):
//   - A Jenkins agent with Python 3.11+ (matching pyproject.toml's
//     requires-python) available on PATH. Provisioning that agent is
//     infrastructure setup outside this file's scope, exactly as
//     .github/workflows/ci.yml assumes actions/setup-python's underlying
//     runner exists without this project provisioning it.
//   - A Unix-like agent (sh steps). A Windows agent would need bat/
//     powershell steps instead — not written here, since no concrete
//     Jenkins agent has been provisioned for this project to target.
//   - `pip install --user` is used rather than a bare global install:
//     unlike GitHub's ephemeral hosted runners, a Jenkins agent is often
//     long-lived/shared across builds, so a per-user install is the safer
//     default absent a known-clean/containerized agent.
//   - Durable test-account credentials (docs/09-Automation-Scope.md
//     §12/§30 item 4) are deliberately NOT wired via Jenkins
//     `credentials()` bindings here: doing so would require a credential
//     ID that does not exist in any Jenkins credential store, since no
//     Jenkins instance has been configured for this project (per
//     instruction: do not invent Jenkins credentials/controllers/agents).
//     No currently implemented test consumes them regardless (only the 9
//     blocked cases would). Left unset, matching Settings' safe empty
//     default and the still-open BLK-001/BLK-002 blockers
//     (docs/18-Defect-Documentation.md §7).

pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    // Mirrors the marker-expression selection already used by
    // .github/workflows/ci.yml. The parameter can only ever filter WITHIN
    // the existing, already-collected 50-test suite via the 8 markers
    // already registered in pyproject.toml (docs/11 §27) — it cannot
    // introduce new test scope by construction, since pytest -m only
    // selects among tests that already exist and are already marked.
    parameters {
        string(
            name: 'MARKER_EXPRESSION',
            defaultValue: 'regression and not ci_restricted',
            description: 'pytest -m expression. Default matches the PR/Main tier in .github/workflows/ci.yml: the 22 currently implemented, approved cases, always excluding the CI-RESTRICTED (blocked, unimplemented) tier. Use "regression" for the full-set/nightly-equivalent tier, or "cross_browser" for the curated release-tier subset.'
        )
        choice(
            name: 'BROWSER',
            choices: ['chromium', 'firefox', 'webkit'],
            description: 'Matches docs/10-Automation-Strategy.md §17: Chromium is the PR/Main/Nightly default; Firefox/WebKit are release-tier only, for the curated cross_browser subset.'
        )
        booleanParam(
            name: 'RUN_FOUNDATION_CHECKS',
            defaultValue: true,
            description: 'Run Tier 1 framework/infrastructure health checks (docs/17-Execution-Report.md §6) before the business regression suite.'
        )
    }

    environment {
        // Public AUT URLs, not secrets — matches .env.example.
        AUT_BASE_URL = 'https://automationexercise.com'
        API_BASE_URL = 'https://automationexercise.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python Runtime') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m pip --version'
            }
        }

        // Single source of truth: pyproject.toml's [project.dependencies].
        // No [build-system] table exists (the project is not packaged), so
        // dependencies are read directly with the stdlib tomllib (Python
        // 3.11+) rather than duplicating the pinned version list into this
        // file — identical technique to .github/workflows/ci.yml.
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade --user pip
                    python3 -m pip install --user $(python3 -c "import tomllib; print(' '.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")
                '''
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                sh "python3 -m playwright install --with-deps ${params.BROWSER}"
            }
        }

        stage('Framework Foundation Checks (Tier 1)') {
            when {
                expression { return params.RUN_FOUNDATION_CHECKS }
            }
            steps {
                sh 'python3 -m pytest tests/test_setup_validation.py tests/test_framework_foundation.py -v -m "not requires_all_browsers"'
            }
        }

        // CI-only bounded retries (docs/10 §16, docs/11 §30: the cited
        // {ci: 2, local: 0} precedent) — identical policy and values to
        // .github/workflows/ci.yml. No -n/xdist parallelism, for the same
        // durable "favor reliability over speed against a single shared
        // public AUT" reasoning (docs/10 §21, docs/11 §29), reinforced by
        // the network instability documented as OBS-001
        // (docs/18-Defect-Documentation.md).
        //
        // A non-zero pytest exit code fails this `sh` step, which fails
        // this stage, which fails the overall build — native Jenkins
        // failure propagation, no custom exit-code handling needed.
        stage('Run Approved Automated Regression Suite') {
            steps {
                sh """
                    python3 -m pytest -m "${params.MARKER_EXPRESSION}" --browser=${params.BROWSER} \
                        --reruns 2 --reruns-delay 3 -v \
                        --html=reports/html/regression-jenkins.html --self-contained-html
                """
            }
        }
    }

    post {
        // Evidence preserved regardless of outcome (docs/10 §15/§19):
        // HTML report every run, screenshots on UI failure, traces on
        // retry-then-fail. allowEmptyArchive: screenshots/traces only
        // exist when a test actually failed. Logs are Jenkins' own console
        // output (src/utils/logger.py writes to stdout, no file handler)
        // — already retained natively by the build's Console Output, no
        // separate log-file archive needed.
        always {
            archiveArtifacts artifacts: 'reports/html/**, reports/screenshots/**, reports/traces/**',
                              allowEmptyArchive: true,
                              fingerprint: false

            // publishHTML (HTML Publisher Plugin) is an optional
            // convenience, not assumed installed on any concrete Jenkins
            // instance (per instruction: do not assume Jenkins is
            // configured with specific plugins). Wrapped so its absence
            // never fails the build — archiveArtifacts above is the
            // load-bearing evidence-preservation mechanism either way.
            script {
                try {
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/html',
                        reportFiles: 'regression-jenkins.html',
                        reportName: 'Pytest HTML Report'
                    ])
                } catch (err) {
                    echo "publishHTML unavailable (HTML Publisher Plugin not installed) — evidence is still preserved via archiveArtifacts above. ${err}"
                }
            }
        }

        success {
            echo "Approved automated regression suite passed (marker: '${params.MARKER_EXPRESSION}', browser: ${params.BROWSER})."
        }

        failure {
            echo "Build failed. Per docs/17-Execution-Report.md's established methodology, a failure must be investigated and classified (Test / Application / Environment / Automation / Data — docs/10-Automation-Strategy.md §26) using the archived evidence before being treated as an AUT or automation defect. This pipeline does not perform automatic failure classification."
        }

        cleanup {
            // Workspace cleanup. deleteDir() is a Jenkins core step (no
            // plugin dependency), consistent with not assuming any
            // specific plugin is installed.
            deleteDir()
        }
    }
}
