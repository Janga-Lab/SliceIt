(function () {



    var columnDefs = [

        {
            headerName: 'Binding Site Information',
            children: [
                {
                    headerName: "CHR", field: "binding_chr", width: 70
                },
                {
                    headerName: "START", field: "binding_start", width: 100
                },
                {
                    headerName: "STOP", field: "binding_stop", width: 150
                },
                {
                    headerName: "GENE", field: "binding_gene",columnGroupShow: 'open', width: 150
                },
                {
                    headerName: "CELL LINE", field: "binding_cl",columnGroupShow: 'open', width: 150
                },
                {
                    headerName: "STRAND", field: "binding_strand",columnGroupShow: 'open', width: 100
                }
            ]
        },
        {
            headerName: 'Exon Expression Information',
            children:  [
                {
                    headerName: "CHR", field: "exon_chr", width: 70
                },
                {
                    headerName: "START", field: "exon_start", width: 100
                },
                {
                    headerName: "STOP", field: "exon_STOP", width: 150
                },
                {
                    headerName: "STRAND", field: "exon_strand",columnGroupShow: 'open'
                },
                {
                    headerName: "MIN", field: "exon_min",columnGroupShow: 'open'
                },
                {
                    headerName: "MAX", field: "exon_max",columnGroupShow: 'open'
                },
                {
                    headerName: "SUM", field: "exon_sum",columnGroupShow: 'open'
                }
            ]
        },
        {
            headerName: 'Guide RNA Information',
            children:  [
                {
                    headerName: "sgRNA_CHR", field: "sgrna_chr", columnGroupShow: 'open'
                },
                {
                    headerName: "sgRNA_START", field: "sgrna_start", columnGroupShow: 'open'
                },
                {
                    headerName: "sgRNA_STOP", field: "sgrna_STOP", columnGroupShow: 'open'
                },
                {
                    headerName: "ORIENTATION", field: "sgrna_orientation",columnGroupShow: 'open'
                },
				{
                    headerName: "LENGTH", field: "sgrna_length",columnGroupShow: 'open'
                },
				{
                    headerName: "sgRNA+PAM+7bpFlank", field: "sgrna_flank",columnGroupShow: 'open'
                },

                {
                    headerName: "sgRNA_Cor(hg19_4_navigation)", field: "sgrna_cor",columnGroupShow: 'open'
                },
                {
                    headerName: "Distance_of_PAM_from_BS_mid", field: "sgrna_distance",columnGroupShow: 'open'
                },
                {
                    headerName: "EFFICIENCY", field: "sgrna_efficiency",columnGroupShow: 'open'
                },
				
                {
                    headerName: "SPECIFICITY", field: "sgrna_specificity",columnGroupShow: 'open'
                },
                {
                    headerName: "sgRNA_DHS_overlap", field: "sgrna_dhs",columnGroupShow: 'open'
                },
                {
                    headerName: "BS_CHR", field: "bs_chr", width: 100
                },
                {
                    headerName: "BS_START", field: "bs_start", width: 100
                },
                {
                    headerName: "BS_STOP", field: "bs_stop", width: 100
                },
                {
                    headerName: "BS_LENGTH	", field: "sgrna_length",columnGroupShow: 'open'
                },
                {
                    headerName: "RBP", field: "sgrna_rbp",columnGroupShow: 'open'
                },
                {
                    headerName: "CELL TYPE", field: "sgrna_celltype",columnGroupShow: 'open'
                }
            ]
        },
        {
            headerName: 'Peek Liver Information',
            children:  [
                {
                    headerName: "Binding Site", field: "peek_bs", width: 200
                },
                {
                    headerName: "Gene of Binding Site", field: "peek_gene",columnGroupShow: 'open'
                },
                {
                    headerName: "Exon", field: "peek_exon",columnGroupShow: 'open'
                },
                {
                    headerName: "Gene_Exon", field: "peek_gene_exon",columnGroupShow: 'open'
                },
                {
                    headerName: "P-Value", field: "peek_pval",columnGroupShow: 'open'
                },
                {
                    headerName: "FDR", field: "peek_fdr",columnGroupShow: 'open'
                }
            ]
        },
        {
            headerName: 'GWAS',
            children:  [
                {
                    headerName: "PVALUE_MLOG", field: "gwas_pvalue_mlog",columnGroupShow: 'open'
                },
                {
                    headerName: "OR or BETA", field: "gwas_or_beta",columnGroupShow: 'open'
                },
                {
                    headerName: "SNP_GENE_IDS", field: "gwas_snp_gene_id",columnGroupShow: 'open'
                },
                {
                    headerName: "DISEASE/TRAIT", field: "gwas_disease_trait",columnGroupShow: 'open'
                },
                {
                    headerName: "MAPPED_TRAIT_URI", field: "gwas_mapped_trait_uri",columnGroupShow: 'open'
                },
                {
                    headerName: "MAPPED_TRAIT", field: "gwas_mapped_trait",columnGroupShow: 'open'
                },
                {
                    headerName: "LINK", field: "gwas_link",columnGroupShow: 'open'
                },
                {
                    headerName: "CONTEXT", field: "gwas_context",columnGroupShow: 'open'
                },
                {
                    headerName: "DATE", field: "gwas_date",columnGroupShow: 'open'
                },
                {
                    headerName: "P-Value (TEXT)", field: "gwas_p_value_text",columnGroupShow: 'open'
                },
                {
                    headerName: "95% CI (TEXT)", field: "gwas_95ci_text",columnGroupShow: 'open'
                },
                {
                    headerName: "FIRST AUTHOR", field: "gwas_first_author",columnGroupShow: 'open'
                },
                {
                    headerName: "CHR_ID", field: "gwas_chr_id",columnGroupShow: 'open'
                },
                {
                    headerName: "INTERGENIC", field: "gwas_intergenic",columnGroupShow: 'open'
                },
                {
                    headerName: "PUBMED ID", field: "gwas_pubmedid",columnGroupShow: 'open'
                },
                {
                    headerName: "UPSTREAM_GENE_ID", field: "gwas_upstream_geneid",columnGroupShow: 'open'
                },
                {
                    headerName: "SNP_ID_CURRENT", field: "gwas_snp_id_current", columnGroupShow: 'open'
                },
                {
                    headerName: "STUDY", field: "gwas_study", columnGroupShow: 'open'
                },
                {
                    headerName: "MERGED", field: "gwas_merged",columnGroupShow: 'open'
                },
				{
                    headerName: "CNV", field: "gwas_cnv",columnGroupShow: 'open'
                },
				{
                    headerName: "SNPS", field: "gwas_snps",columnGroupShow: 'open'
                },
                {
                    headerName: "PLATFORM [SNPS PASSING QC] : Illumina [318237]", field: "gwas_platform_illumina",columnGroupShow: 'open'
                },
                {
                    headerName: "INITIAL SAMPLE SIZE", field: "gwas_initial_sample_size",columnGroupShow: 'open'
                },
                {
                    headerName: "RISK ALLELE FREQUENCY", field: "gwas_risk_allele",columnGroupShow: 'open'
                },
				
                {
                    headerName: "CHR_POS", field: "gwas_chr_pos", width: 200
                },
                {
                    headerName: "MAPPED_GENE", field: "gwas_mapped_gene",columnGroupShow: 'open'
                },
                {
                    headerName: "P-VALUE", field: "gwas_p_value",columnGroupShow: 'open'
                },
                {
                    headerName: "DOWNSTREAM GENE ID", field: "gwas_downstream_geneid",columnGroupShow: 'open'
                },
                {
                    headerName: "STRONGEST SNP-RISK ALLELE", field: "gwas_strongest_snp",columnGroupShow: 'open'
                },
                {
                    headerName: "STUDY ACCESSION", field: "gwas_study_acession",columnGroupShow: 'open'
                },
                {
                    headerName: "REPORTED GENE(S)", field: "gwas_reported_genes",columnGroupShow: 'open'
                },
                {
                    headerName: "JOURNAL", field: "gwas_journal",columnGroupShow: 'open'
                },
                {
                    headerName: "REPLICATION SAMPLE SIZE", field: "gwas_replication_sample",columnGroupShow: 'open'
                },
				
                {
                    headerName: "DATE ADDED TO CATALOG", field: "gwas_data_catalog",columnGroupShow: 'open'
                },
                {
                    headerName: "UPSTREAM_GENE_DISTANCE", field: "gwas_upstream_genedistance",columnGroupShow: 'open'
                },
                {
                    headerName: "DOWNSTREAM_GENE_DISTANCE", field: "gwas_downstream_genedistance",columnGroupShow: 'open'
                },
                {
                    headerName: "REGION", field: "gwas_region", width: 100
                }
            ]
        }
    ];

    var gridOptions = {
        columnDefs: columnDefs,
        rowSelection: 'multiple',
        enableColResize: true,
        enableSorting: true,
        enableFilter: true,
        enableRangeSelection: true,
        suppressRowClickSelection: true,
        animateRows: true,
        onModelUpdated: modelUpdated,
        debug: true
    };
	
	function onBtExport() {
    var params = {
        skipHeader: getBooleanValue('#skipHeader'),
        columnGroups: getBooleanValue('#columnGroups'),
        skipFooters: getBooleanValue('#skipFooters'),
        skipGroups: getBooleanValue('#skipGroups'),
        skipPinnedTop: getBooleanValue('#skipPinnedTop'),
        skipPinnedBottom: getBooleanValue('#skipPinnedBottom'),
        allColumns: getBooleanValue('#allColumns'),
        onlySelected: getBooleanValue('#onlySelected'),
        suppressQuotes: getBooleanValue('#suppressQuotes'),
        fileName: document.querySelector('#fileName').value,
        columnSeparator: document.querySelector('#columnSeparator').value
    };

    if (getBooleanValue('#skipGroupR')) {
        params.shouldRowBeSkipped = function(params) {
            return params.node.data.country.charAt(0) === 'R';
        };
    }

    if (getBooleanValue('#useCellCallback')) {
        params.processCellCallback = function(params) {
            if (params.value && params.value.toUpperCase) {
                return params.value.toUpperCase();
            } else {
                return params.value;
            }
        };
    }

    if (getBooleanValue('#useSpecificColumns')) {
        params.columnKeys = ['country', 'bronze'];
    }

    if (getBooleanValue('#processHeaders')) {
        params.processHeaderCallback = function(params) {
            return params.column.getColDef().headerName.toUpperCase();
        };
    }

    if (getBooleanValue('#customHeader')) {
        params.customHeader = '[[[ This ia s sample custom header - so meta data maybe?? ]]]\n';
    }
    if (getBooleanValue('#customFooter')) {
        params.customFooter = '[[[ This ia s sample custom footer - maybe a summary line here?? ]]]\n';
    }

    gridOptions.api.exportDataAsCsv(params);
}

    var btBringGridBack;
    var btDestroyGrid;

    // wait for the document to be loaded, otherwise
    // ag-Grid will not find the div in the document.
    document.addEventListener("DOMContentLoaded", function () {
        btBringGridBack = document.querySelector('#btBringGridBack');
        btDestroyGrid = document.querySelector('#btDestroyGrid');

        // this example is also used in the website landing page, where
        // we don't display the buttons, so we check for the buttons existance
        if (btBringGridBack) {
            btBringGridBack.addEventListener('click', onBtBringGridBack);
            btDestroyGrid.addEventListener('click', onBtDestroyGrid);
        }

        addQuickFilterListener();
        onBtBringGridBack();
    });

	
	
	
    function onBtBringGridBack() {
        var eGridDiv = document.querySelector('#bestHtml5Grid');
        new agGrid.Grid(eGridDiv, gridOptions);
        if (btBringGridBack) {
            btBringGridBack.disabled = true;
            btDestroyGrid.disabled = false;
        }
        // createRowData is available in data.js
        gridOptions.api.setRowData(createRowData());
    }

    function onBtDestroyGrid() {
        btBringGridBack.disabled = false;
        btDestroyGrid.disabled = true;
        gridOptions.api.destroy();
    }

    function addQuickFilterListener() {
        var eInput = document.querySelector('#quickFilterInput');
        eInput.addEventListener("input", function () {
            var text = eInput.value;
            gridOptions.api.setQuickFilter(text);
        });
    }

    function modelUpdated() {
        var model = gridOptions.api.getModel();
        var totalRows = model.getTopLevelNodes().length;
        var processedRows = model.getRowCount();
        var eSpan = document.querySelector('#rowCount');
        eSpan.innerHTML = processedRows.toLocaleString() + ' / ' + totalRows.toLocaleString();
    }

    function skillsCellRenderer(params) {
        var data = params.data;
        var skills = [];
        IT_SKILLS.forEach(function (skill) {
            if (data && data.skills[skill]) {
                skills.push('<img src="https://www.ag-grid.com/images/skills/' + skill + '.png" width="16px" title="' + skill + '" />');
            }
        });
        return skills.join(' ');
    }

    function countryCellRenderer(params) {
        var flag = "<img border='0' width='15' height='10' style='margin-bottom: 2px' src='https://flags.fmcdn.net/data/flags/mini/" + COUNTRY_CODES[params.value] + ".png'>";
        return flag + " " + params.value;
    }

    function createRandomPhoneNumber() {
        var result = '+';
        for (var i = 0; i < 12; i++) {
            result += Math.round(Math.random() * 10);
            if (i === 2 || i === 5 || i === 8) {
                result += ' ';
            }
        }
        return result;
    }

    function percentCellRenderer(params) {
        var value = params.value;

        var eDivPercentBar = document.createElement('div');
        eDivPercentBar.className = 'div-percent-bar';
        eDivPercentBar.style.width = value + '%';
        if (value < 20) {
            eDivPercentBar.style.backgroundColor = '#f44336';
        } else if (value < 60) {
            eDivPercentBar.style.backgroundColor = '#FF9100';
        } else {
            eDivPercentBar.style.backgroundColor = '#4CAF50';
        }

        var eValue = document.createElement('div');
        eValue.className = 'div-percent-value';
        eValue.innerHTML = value + '%';

        var eOuterDiv = document.createElement('div');
        eOuterDiv.className = 'div-outer-div';
        eOuterDiv.appendChild(eDivPercentBar);
        eOuterDiv.appendChild(eValue);

        return eOuterDiv;
    }

    var SKILL_TEMPLATE =
        '<label style="border: 1px solid lightgrey; margin: 4px; padding: 4px; display: inline-block;">' +
        '  <span>' +
        '    <div style="text-align: center;">SKILL_NAME</div>' +
        '    <div>' +
        '      <input type="checkbox"/>' +
        '      <img src="https://www.ag-grid.com/images/skills/SKILL.png" width="30px"/>' +
        '    </div>' +
        '  </span>' +
        '</label>';

    var FILTER_TITLE =
        '<div style="text-align: center; background: lightgray; width: 100%; display: block; border-bottom: 1px solid grey;">' +
        '<b>TITLE_NAME</b>' +
        '</div>';

    function SkillFilter() {
    }

    SkillFilter.prototype.init = function (params) {
        this.filterChangedCallback = params.filterChangedCallback;
        this.model = {
            android: false,
            css: false,
            html5: false,
            mac: false,
            windows: false
        };
    };

    SkillFilter.prototype.getModel = function () {

    };

    SkillFilter.prototype.setModel = function (model) {

    };

    SkillFilter.prototype.getGui = function () {
        var eGui = document.createElement('div');
        var eInstructions = document.createElement('div');
        eInstructions.innerHTML = FILTER_TITLE.replace('TITLE_NAME', 'Custom Skills Filter');
        eGui.appendChild(eInstructions);

        var that = this;

        IT_SKILLS.forEach(function (skill, index) {
            var skillName = IT_SKILLS_NAMES[index];
            var eSpan = document.createElement('span');
            var html = SKILL_TEMPLATE.replace("SKILL_NAME", skillName).replace("SKILL", skill);
            eSpan.innerHTML = html;

            var eCheckbox = eSpan.querySelector('input');
            eCheckbox.addEventListener('click', function () {
                that.model[skill] = eCheckbox.checked;
                that.filterChangedCallback();
            });

            eGui.appendChild(eSpan);
        });

        return eGui;
    };

    SkillFilter.prototype.doesFilterPass = function (params) {

        var rowSkills = params.data.skills;
        var model = this.model;
        var passed = true;

        IT_SKILLS.forEach(function (skill) {
            if (model[skill]) {
                if (!rowSkills[skill]) {
                    passed = false;
                }
            }
        });

        return passed;
    };

    SkillFilter.prototype.isFilterActive = function () {
        var model = this.model;
        var somethingSelected = model.android || model.css || model.html5 || model.mac || model.windows;
        return somethingSelected;
    };

    var PROFICIENCY_TEMPLATE =
        '<label style="padding-left: 4px;">' +
        '<input type="radio" name="RANDOM"/>' +
        'PROFICIENCY_NAME' +
        '</label>';

    var PROFICIENCY_NONE = 'none';
    var PROFICIENCY_ABOVE40 = 'above40';
    var PROFICIENCY_ABOVE60 = 'above60';
    var PROFICIENCY_ABOVE80 = 'above80';

    var PROFICIENCY_NAMES = ['No Filter', 'Above 40%', 'Above 60%', 'Above 80%'];
    var PROFICIENCY_VALUES = [PROFICIENCY_NONE, PROFICIENCY_ABOVE40, PROFICIENCY_ABOVE60, PROFICIENCY_ABOVE80];

    function ProficiencyFilter() {
    }

    ProficiencyFilter.prototype.init = function (params) {
        this.filterChangedCallback = params.filterChangedCallback;
        this.selected = PROFICIENCY_NONE;
        this.valueGetter = params.valueGetter;
    };

    ProficiencyFilter.prototype.getModel = function () {

    };

    ProficiencyFilter.prototype.setModel = function (model) {

    };

    ProficiencyFilter.prototype.getGui = function () {
        var eGui = document.createElement('div');
        var eInstructions = document.createElement('div');
        eInstructions.innerHTML = FILTER_TITLE.replace('TITLE_NAME', 'Custom Proficiency Filter');
        eGui.appendChild(eInstructions);

        var random = '' + Math.random();

        var that = this;
        PROFICIENCY_NAMES.forEach(function (name, index) {
            var eFilter = document.createElement('div');
            var html = PROFICIENCY_TEMPLATE.replace('PROFICIENCY_NAME', name).replace('RANDOM', random);
            eFilter.innerHTML = html;
            var eRadio = eFilter.querySelector('input');
            if (index === 0) {
                eRadio.checked = true;
            }
            eGui.appendChild(eFilter);

            eRadio.addEventListener('click', function () {
                that.selected = PROFICIENCY_VALUES[index];
                that.filterChangedCallback();
            });
        });

        return eGui;
    };

    ProficiencyFilter.prototype.doesFilterPass = function (params) {

        var value = this.valueGetter(params);
        var valueAsNumber = parseFloat(value);

        switch (this.selected) {
            case PROFICIENCY_ABOVE40 :
                return valueAsNumber >= 40;
            case PROFICIENCY_ABOVE60 :
                return valueAsNumber >= 60;
            case PROFICIENCY_ABOVE80 :
                return valueAsNumber >= 80;
            default :
                return true;
        }

    };

    ProficiencyFilter.prototype.isFilterActive = function () {
        return this.selected !== PROFICIENCY_NONE;
    };
})();
