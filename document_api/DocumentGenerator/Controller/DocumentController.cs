namespace DocumentGenerator.Controller
{
    using DocumentGenerator.Models;
    using Microsoft.AspNetCore.Mvc;
    using System.IO;
    using iText.Html2pdf;
    using iText.Kernel.Pdf;
    using iText.Kernel.Utils;

    [ApiController]
    [Route("api/document")]
    public class DocumentController : ControllerBase
    {
        const string FOLDER = @"Assets";
        const string SURVEY_TEMPPLATE = $@"{FOLDER}/SurveyTest.html";
        const string DOCUMENT_SURVEY = $@"{FOLDER}/DocumentSurvey.pdf";
        public DocumentController()
        {

        }

        [HttpGet]
        public ActionResult Get()
        {
            return Ok("Document Service is Running!");
        }

        [HttpPost]
        [Route("create")]
        public async Task<ActionResult> GenerateSurvey([FromBody] Survey survey)
        {
            var response = await CreateSurvey(survey);
            return Ok(response);
        }

        private async Task<SurveyResponse> CreateSurvey(Survey survey)
        {
            var response = new SurveyResponse { Location = DOCUMENT_SURVEY};
            var surveyTemplate = Path.GetFullPath(SURVEY_TEMPPLATE);
            var memoryStream = new MemoryStream(await System.IO.File.ReadAllBytesAsync(surveyTemplate));
            var surveyComplete = ReplaceSurveyValues(await new StreamReader(memoryStream).ReadToEndAsync(), survey);

            var stream = new MemoryStream();
            HtmlConverter.ConvertToPdf(surveyComplete, stream);
            SaveFile(DOCUMENT_SURVEY, stream);
            return response;
        }

        private string ReplaceSurveyValues(string template, Survey survey)
        {
            template = template.Replace("[NAME]", survey.Name);
            template = template.Replace("[LASTNAME]", survey.LastName);
            return template;
        }

        private void SaveFile(string fileName, MemoryStream stream)
        {
            var memoryStream = new MemoryStream(stream.ToArray());
            memoryStream.Seek(0, SeekOrigin.Begin);
            var fileStream = System.IO.File.Create(fileName);
            memoryStream.CopyTo(fileStream);
            fileStream.Close();
        }
    }
}