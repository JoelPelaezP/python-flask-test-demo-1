namespace DocumentGenerator.Controller
{
    using System;
    using DocumentGenerator.Models;
    using Microsoft.AspNetCore.Mvc;
    using System.IO;

    [ApiController]
    [Route("api/document")]
    public class DocumentController : ControllerBase
    {
        const string SURVEY_TEMPPLATE = "Assets/SurveyTest.html";
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
            var response = new SurveyResponse { Location = "Dummy.pdf" };
            var surveyTemplate = Path.GetFullPath(SURVEY_TEMPPLATE);
            var memoryStream = new MemoryStream(await System.IO.File.ReadAllBytesAsync(surveyTemplate));
            var surveyComplete = ReplaceSurveyValues(await new StreamReader(memoryStream).ReadToEndAsync(), survey);

            return response;
        }

        private string ReplaceSurveyValues(string template, Survey survey)
        {
            template = template.Replace("[NAME]", survey.Name);
            template = template.Replace("[LASTNAME]", survey.LastName);
            return template;
        }
    }
}