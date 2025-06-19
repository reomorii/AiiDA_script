from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, List, Str

class lsCalculation(CalcJob):
    """AiiDA calculation plugin wrapping the diff executable."""
    @classmethod
    def define(cls, spec):
        super(lsCalculation, cls).define(spec)
        
        #new ports
        spec.input('directory_path', valid_type=Str, help='Path of the directory to list.') #ディレクトリのpahtを指定
        # spec.output('ls_output', valid_type=SinglefileData, help='Output of the ls command.') #lsコマンドの出力
        spec.output('ls_output', valid_type=List, help='Output of the ls command.') #lsコマンドの出力

        spec.input('metadata.options.output_filename', valid_type=str, default='ls.txt')
        spec.inputs['metadata']['options']['resources'].default = {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        }
        spec.inputs['metadata']['options']['parser_name'].default = 'ls-tutorial'

        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')

    def prepare_for_submission(self, folder):
        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = ['-1', self.inputs.directory_path.value]
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename

        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        # calcinfo.local_copy_list = [self.inputs.directory_path.uuid, self.inputs.directory_path.value, self.inputs.directory_path.value]
        calcinfo.retrieve_list = [self.inputs.metadata.options.output_filename]

        return calcinfo
