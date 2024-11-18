from aiida.engine import ExitCode
from aiida.orm import SinglefileData, List
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

DiffCalculation = CalculationFactory('ls-tutorial')


class lsParser(Parser):
    def parse(self, **kwargs):
        """Parse outputs, store results in database.

        :returns: non-zero exit code, if parsing fails
        """
        output_filename = self.node.get_option('output_filename')

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = [output_filename]
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(f"Found files '{files_retrieved}', expected to find '{files_expected}'")
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        # self.logger.info(f"Parsing '{output_filename}'")
        # with self.retrieved.open(output_filename, 'rb') as handle:
        #     output_node = SinglefileData(file=handle)
        
        with self.retrieved.open(output_filename, 'r') as handle:
            lines = handle.read().splitlines()
            output_node = List(list=lines)
        
        self.out('ls_output', output_node)

        return ExitCode(0)